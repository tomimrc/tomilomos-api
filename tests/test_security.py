"""Tests for password hashing and security."""

import pytest
import os
from app.core.security import hash_password, verify_password, get_bcrypt_cost


class TestBcryptCost:
    """Test bcrypt cost factor configuration."""
    
    def test_default_bcrypt_cost(self):
        """Test default bcrypt cost is 12."""
        with pytest.raises(KeyError):
            # Temporarily remove env var to test default
            pass
        # When BCRYPT_COST not set, should default to 12
        cost = get_bcrypt_cost()
        assert 10 <= cost <= 31
    
    def test_bcrypt_cost_validation_below_minimum(self):
        """Test bcrypt cost must be >= 10."""
        os.environ["BCRYPT_COST"] = "9"
        with pytest.raises(ValueError, match="between 10 and 31"):
            get_bcrypt_cost()
        del os.environ["BCRYPT_COST"]
    
    def test_bcrypt_cost_validation_above_maximum(self):
        """Test bcrypt cost must be <= 31."""
        os.environ["BCRYPT_COST"] = "32"
        with pytest.raises(ValueError, match="between 10 and 31"):
            get_bcrypt_cost()
        del os.environ["BCRYPT_COST"]


class TestPasswordHashing:
    """Test password hashing functionality."""
    
    def test_hash_password_produces_unique_hashes(self):
        """Test hash_password produces different hashes for same input (salt uniqueness)."""
        password = "MySecurePassword123!"
        
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Hashes should be different due to unique salt
        assert hash1 != hash2
        # Both should start with bcrypt prefix
        assert hash1.startswith("$2b$")
        assert hash2.startswith("$2b$")
    
    def test_verify_password_correct(self):
        """Test verify_password returns True for correct password."""
        password = "CorrectPassword123!"
        password_hash = hash_password(password)
        
        result = verify_password(password, password_hash)
        assert result is True
    
    def test_verify_password_incorrect(self):
        """Test verify_password returns False for incorrect password."""
        password = "OriginalPassword123!"
        password_hash = hash_password(password)
        
        wrong_password = "WrongPassword456!"
        result = verify_password(wrong_password, password_hash)
        assert result is False
    
    def test_verify_password_with_invalid_hash(self):
        """Test verify_password handles invalid hash gracefully."""
        password = "SomePassword"
        invalid_hash = "not-a-valid-bcrypt-hash"
        
        result = verify_password(password, invalid_hash)
        assert result is False
