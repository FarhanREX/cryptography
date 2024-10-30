from Crypto.Cipher import DES
import os
import struct

# Function to XOR two byte strings
def xor_bytes(data1, data2):
    return bytes(a ^ b for a, b in zip(data1, data2))

# Incrementing the counter
def increment_counter(counter):
    # Unpack the counter as a 64-bit big-endian integer, increment it, and pack it back
    counter_int = struct.unpack('>Q', counter)[0]  # Convert bytes to an integer
    counter_int += 1                               # Increment the integer
    return struct.pack('>Q', counter_int)          # Convert back to bytes

# DES-CTR encryption function
def des_ctr_encrypt(plaintext, key, nonce):
    # Generate a random 4-byte IV (Initialization Vector)
    iv = os.urandom(4)
    
    # Initialize the counter with the nonce and IV
    counter = nonce + iv
    
    # Create a DES cipher object in ECB mode for counter encryption
    cipher = DES.new(key, DES.MODE_ECB)
    
    ciphertext = b""
    
    # Encrypt the plaintext block by block
    for i in range(0, len(plaintext), 8):
        # Get the next 8-byte block of plaintext (pad with zeros if necessary)
        block = plaintext[i:i+8].ljust(8, b'\0')
        
        # Encrypt the current counter value
        encrypted_counter = cipher.encrypt(counter)
        
        # XOR the encrypted counter with the plaintext block
        encrypted_block = xor_bytes(block, encrypted_counter)
        
        # Append the encrypted block to the ciphertext
        ciphertext += encrypted_block
        
        # Increment the counter for the next block
        counter = increment_counter(counter)
    
    # Return nonce + IV + ciphertext for decryption
    return nonce + iv + ciphertext

# DES-CTR decryption function
def des_ctr_decrypt(ciphertext, key):
    # Extract nonce, IV, and ciphertext separately
    nonce = ciphertext[:4]
    iv = ciphertext[4:8]
    ciphertext = ciphertext[8:]
    
    # Initialize the counter with the nonce and IV
    counter = nonce + iv
    
   
    cipher = DES.new(key, DES.MODE_ECB)
    
    plaintext = b""
    
    # Decrypt the ciphertext block by block
    for i in range(0, len(ciphertext), 8):
        # Get the next 8-byte block of ciphertext
        block = ciphertext[i:i+8]
        
        # Encrypt the current counter value
        encrypted_counter = cipher.encrypt(counter)
        
        # XOR the encrypted counter with the ciphertext block
        decrypted_block = xor_bytes(block, encrypted_counter)
        
        # Append the decrypted block to the plaintext
        plaintext += decrypted_block
        
        # Increment the counter for the next block
        counter = increment_counter(counter)
    
    return plaintext.rstrip(b'\0')  # Remove padding

# Example usage
key = os.urandom(8)  # DES key must be 8 bytes long
nonce = os.urandom(4)  # Random nonce (4 bytes)

plaintext = b'This is a secret message that needs to be encrypted.'

# Encrypt the plaintext
ciphertext = des_ctr_encrypt(plaintext, key, nonce)
print("Ciphertext:", ciphertext)

# Decrypt the ciphertext
decrypted = des_ctr_decrypt(ciphertext, key)
print("Decrypted:", decrypted.decode('utf-8'))
