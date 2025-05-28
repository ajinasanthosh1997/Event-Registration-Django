# utils.py
import random
import string

def generate_otp(length=6):
    """Generate a random OTP of the specified length."""
    characters = string.digits  # Use digits for numeric OTP
    otp = ''.join(random.choice(characters) for i in range(length))
    return otp
