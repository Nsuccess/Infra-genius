# InfraGenius Agent Startup Script
# Set your API keys before running

# LLM Provider (Nebius)
$env:CUSTOM_API_KEY="your-nebius-api-key-here"

# E2B for cloud sandboxes
$env:E2B_API_KEY="your-e2b-api-key-here"

# Start the agent
openagents agent start ./agents/deployer.yaml
