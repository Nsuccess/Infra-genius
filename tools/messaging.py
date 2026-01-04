"""
Messaging tools for sending responses back to the UI.
"""

# Global reference to store the agent client for sending messages
_agent_client = None
_source_id = None

def set_agent_context(agent_client, source_id):
    """Set the agent client and source for messaging."""
    global _agent_client, _source_id
    _agent_client = agent_client
    _source_id = source_id

def send_message(text: str) -> str:
    """
    Send a message back to the user.
    
    Args:
        text: The message text to send
    
    Returns:
        Confirmation that message was sent
    """
    # This is a placeholder - the actual message sending happens
    # through the agent framework when this tool returns
    return f"Message sent: {text}"
