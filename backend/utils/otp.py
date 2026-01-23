import time          # Used to get current system time
import hmac          # Used to create HMAC (Hash-based Message Authentication Code)
import hashlib       # Provides cryptographic hash functions (SHA-1)
import struct        # Used to convert numbers into binary format
import base64        # Used because OTP secrets are stored in Base32 format
import os

def generate_totp(secret, time_step=120, digits=6):
    """ Generates a Time-Based One-Time Password (TOTP)
        secret    → shared secret key between server and user
        time_step → how long each OTP is valid (default 30 seconds)
        digits    → length of OTP (default 6 digits)  """

    # Decode the Base32 secret (used by Google Authenticator) into raw bytes
    key = base64.b32decode(secret, casefold=True)

    # Get the current Unix time (seconds since 1 Jan 1970)
    current_time = time.time()

    # Convert time into a moving counter (changes every 30 seconds)
    counter = int(current_time // time_step)

    # Convert counter to 8-byte binary format (required for HMAC)
    counter_bytes = struct.pack(">Q", counter)

    # Generate HMAC using SHA-1
    # This creates a cryptographic hash of (secret key + time counter)
    hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()

    # Take the last byte of the hash and extract the lower 4 bits
    # This gives a dynamic offset (0–15)
    offset = hmac_hash[-1] & 0x0F

    # Extract 4 bytes from the hash starting at the offset
    selected_bytes = hmac_hash[offset:offset + 4]

    # Convert those 4 bytes into a 32-bit integer
    # & 0x7FFFFFFF removes the sign bit to make it positive
    binary_number = struct.unpack(">I", selected_bytes)[0] & 0x7FFFFFFF

    # Reduce the large number to the required number of digits (e.g., 6)
    otp = binary_number % (10 ** digits)

    # Convert to string and add leading zeros if needed
    return str(otp).zfill(digits)


def generate_secret():
    # Generate 160 bits (20 bytes) of random data
    random_bytes = os.urandom(20)

    # Convert to Base32 (Google Authenticator format)
    return base64.b32encode(random_bytes).decode("utf-8")


def verify_totp(user_input, secret, time_step=120, digits=4):
    """
    Re-generates OTP from the same secret and checks it
    """
    server_otp = generate_totp(secret, time_step, digits)
    return hmac.compare_digest(user_input, server_otp)

