#!/usr/bin/env python3
import os
import base64
import secrets

def generate_secret_key(method="urandom"):
    """Generate a cryptographically secure secret key.
    
    Args:
        method (str): Method to use for key generation ('urandom' or 'token')
        
    Returns:
        str: A secure secret key
    """
    if method == "urandom":
        # Generate a 32-byte random key and encode it as base64
        return base64.b64encode(os.urandom(32)).decode('utf-8')
    else:
        # Generate a 32-byte hex token
        return secrets.token_hex(32)

if __name__ == "__main__":
    urandom_key = generate_secret_key("urandom")
    token_key = generate_secret_key("token")
    
    print("\nGenerated SECRET_KEY options (choose one):\n")
    print(f"Base64 (urandom): {urandom_key}")
    print(f"Hex (token_hex): {token_key}\n")
    print("Add your chosen key to your environment variables:")
    print("\nFor development (.env file):")
    print(f"SECRET_KEY='{urandom_key}'")
    print("\nFor production (env_variables.yaml):")
    print(f"  SECRET_KEY: '{urandom_key}'\n")
    print("Remember to keep your secret key secure and never commit it to version control!")