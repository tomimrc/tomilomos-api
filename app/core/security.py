"""Password hashing and verification using bcrypt."""

import os
from bcrypt import hashpw, gensalt, checkpw


def get_bcrypt_cost() -> int:
    """Get bcrypt cost factor from environment or use default.
    
    Returns:
        int: Bcrypt cost factor (10-31)
        
    Raises:
        ValueError: If BCRYPT_COST is invalid
    """
    cost_str = os.getenv("BCRYPT_COST", "12")
    try:
        cost = int(cost_str)
    except ValueError:
        raise ValueError(f"BCRYPT_COST must be an integer, got: {cost_str}")
    
    if cost < 10 or cost > 31:
        raise ValueError(f"BCRYPT_COST must be between 10 and 31, got: {cost}")
    
    return cost


def hash_password(password: str) -> str:
    """Hash a password using bcrypt.
    
    Args:
        password: Plaintext password to hash
        
    Returns:
        str: Bcrypt hash with salt included (e.g., $2b$12$...)
    """
    cost = get_bcrypt_cost()
    salt = gensalt(rounds=cost)
    hashed = hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plaintext password against a bcrypt hash using constant-time comparison.
    
    Args:
        password: Plaintext password to verify
        password_hash: Bcrypt hash to check against
        
    Returns:
        bool: True if password matches, False otherwise
    """
    try:
        return checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except (ValueError, TypeError):
        # Invalid hash format or encoding
        return False
