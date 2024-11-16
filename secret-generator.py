import secrets

secret_key = secrets.token_hex(16)  # Generates a random 32-character secret key
print(secret_key)