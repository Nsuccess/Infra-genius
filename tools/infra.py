"""
InfraGenius Tools - Infrastructure Automation for OpenAgents

These tools are auto-discovered by OpenAgents and available to all agents.
Uses the @tool decorator for proper MCP exposure.
"""

import os
import time
from typing import Dict, Any, Optional

# Try to import the tool decorator, fall back to simple function if not available
try:
    from openagents.workspace.tool_decorator import tool
except ImportError:
    # Fallback: create a no-op decorator
    def tool(func=None, *, name=None, description=None, input_schema=None):
        if func is not None:
            return func
        return lambda f: f

# Global sandbox registry
_sandboxes: Dict[str, Any] = {}


@tool(description="Provision a new E2B cloud sandbox for deployment")
def provision_sandbox(name: str) -> str:
    """
    Provision a new E2B sandbox.
    
    Args:
        name: A friendly name for the sandbox (e.g., "deploy-1")
    
    Returns:
        Status message with sandbox ID and URL
    """
    from e2b_code_interpreter import Sandbox
    
    api_key = os.environ.get("E2B_API_KEY")
    if not api_key:
        return "❌ E2B_API_KEY not set. Please configure your API key."
    
    try:
        print(f"🚀 Provisioning sandbox: {name}")
        
        # Use the new Sandbox.create() API (E2B SDK v2.x)
        # API key is read from E2B_API_KEY env var automatically
        sandbox = Sandbox.create(timeout=600)  # 10 minutes
        sandbox_id = sandbox.sandbox_id
        base_url = f"https://8000-{sandbox_id}.e2b.app"
        
        _sandboxes[name] = {
            "sandbox": sandbox,
            "sandbox_id": sandbox_id,
            "base_url": base_url,
            "created_at": time.time(),
        }
        
        return f"✅ Sandbox provisioned!\n📦 Name: {name}\n🆔 ID: {sandbox_id}\n🔗 URL: {base_url}"
        
    except Exception as e:
        return f"❌ Failed to provision sandbox: {str(e)}"


@tool(description="List all active E2B sandboxes")
def list_sandboxes() -> str:
    """
    List all active sandboxes.
    
    Returns:
        Formatted list of active sandboxes
    """
    if not _sandboxes:
        return "📭 No active sandboxes. Use provision_sandbox() to create one."
    
    output = "📦 **Active Sandboxes:**\n\n"
    for name, info in _sandboxes.items():
        output += f"• **{name}**\n"
        output += f"  ID: {info['sandbox_id']}\n"
        output += f"  URL: {info['base_url']}\n\n"
    
    return output


@tool(description="Execute a shell command in an E2B sandbox")
def run_command(sandbox_name: str, command: str) -> str:
    """
    Execute a shell command in a sandbox.
    
    Args:
        sandbox_name: Name of the sandbox
        command: Shell command to execute
    
    Returns:
        Command output
    """
    if sandbox_name not in _sandboxes:
        return f"❌ Sandbox '{sandbox_name}' not found."
    
    sandbox = _sandboxes[sandbox_name]["sandbox"]
    
    try:
        print(f"⚡ Running: {command}")
        result = sandbox.commands.run(command)
        
        output = ""
        if result.stdout:
            output += f"📤 stdout:\n{result.stdout}\n"
        if result.stderr:
            output += f"📤 stderr:\n{result.stderr}\n"
        output += f"🔢 Exit code: {result.exit_code}"
        
        return f"{'✅' if result.exit_code == 0 else '⚠️'} {output}"
            
    except Exception as e:
        return f"❌ Command failed: {str(e)}"


@tool(description="Deploy an app from GitHub to an E2B sandbox (clone, install, build, serve)")
def deploy_app(sandbox_name: str, repo_url: str) -> str:
    """
    Full deployment pipeline: clone → install → build → serve.
    
    Args:
        sandbox_name: Name of the sandbox to deploy to
        repo_url: GitHub repository URL
    
    Returns:
        Deployment status with live URL
    """
    if sandbox_name not in _sandboxes:
        return f"❌ Sandbox '{sandbox_name}' not found. Provision one first."
    
    sandbox = _sandboxes[sandbox_name]["sandbox"]
    base_url = _sandboxes[sandbox_name]["base_url"]
    
    try:
        steps = []
        
        # Step 1: Clone
        print("1️⃣ Cloning repository...")
        result = sandbox.commands.run(f"git clone {repo_url} /home/user/app")
        if result.exit_code != 0:
            return f"❌ Clone failed: {result.stderr}"
        steps.append("✅ Cloned")
        
        # Step 2: Install
        print("2️⃣ Installing dependencies...")
        result = sandbox.commands.run("cd /home/user/app && npm install", timeout=120)
        if result.exit_code != 0:
            return f"❌ Install failed: {result.stderr}"
        steps.append("✅ Installed")
        
        # Step 3: Build
        print("3️⃣ Building...")
        result = sandbox.commands.run("cd /home/user/app && npm run build", timeout=120)
        if result.exit_code != 0:
            return f"❌ Build failed: {result.stderr}"
        steps.append("✅ Built")
        
        # Step 4: Serve
        print("4️⃣ Starting server...")
        sandbox.commands.run(
            "cd /home/user/app/dist && nohup python3 -m http.server 8000 > /tmp/server.log 2>&1 &"
        )
        time.sleep(3)
        
        result = sandbox.commands.run("ps aux | grep 'http.server' | grep -v grep")
        if result.exit_code != 0:
            return "❌ Server failed to start"
        steps.append("✅ Server running")
        
        return f"🎉 **Deployment Complete!**\n\n{chr(10).join(steps)}\n\n🔗 **Live URL:** {base_url}"
        
    except Exception as e:
        return f"❌ Deployment failed: {str(e)}"


@tool(description="Verify a URL is accessible and returns HTTP 200")
def verify_url(url: str) -> str:
    """
    Verify a URL is live.
    
    Args:
        url: URL to verify
    
    Returns:
        Verification status
    """
    import requests
    
    try:
        print(f"🔍 Verifying {url}...")
        start = time.time()
        response = requests.get(url, timeout=10, allow_redirects=True)
        elapsed = (time.time() - start) * 1000
        
        if response.status_code == 200:
            return f"✅ URL is LIVE!\n🔗 {url}\n📊 HTTP {response.status_code}\n⏱️ {elapsed:.0f}ms"
        else:
            return f"⚠️ HTTP {response.status_code}\n🔗 {url}\n⏱️ {elapsed:.0f}ms"
            
    except Exception as e:
        return f"❌ Failed: {str(e)}"


@tool(description="Measure latency to a URL with multiple samples")
def check_latency(url: str, samples: int = 3) -> str:
    """
    Check latency to a URL.
    
    Args:
        url: URL to check
        samples: Number of samples (default 3)
    
    Returns:
        Latency statistics
    """
    import requests
    
    try:
        times = []
        for i in range(samples):
            start = time.time()
            requests.get(url, timeout=10)
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)
        
        avg = sum(times) / len(times)
        return f"📊 Latency: {avg:.0f}ms avg ({min(times):.0f}-{max(times):.0f}ms)"
        
    except Exception as e:
        return f"❌ Failed: {str(e)}"
