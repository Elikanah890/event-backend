import uuid

def generate_invitation_token() -> str:
    """
    Generate a unique invitation token (UUID4) for invitations.
    """
    return str(uuid.uuid4())
