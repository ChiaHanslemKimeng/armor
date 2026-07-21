import os
import base64
import ecdsa

def generate_vapid_keys():
    # Generate ECDSA private key for curve P-256
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
    # Get the public key
    public_key = private_key.get_verifying_key()
    
    # Extract uncompressed public key bytes (65 bytes, starts with \x04)
    public_bytes = b'\x04' + public_key.to_string()
    
    # Extract private key bytes (32 bytes)
    private_bytes = private_key.to_string()
    
    # Base64 urlsafe encode them (stripping padding)
    pub_b64 = base64.urlsafe_b64encode(public_bytes).decode('ascii').rstrip('=')
    priv_b64 = base64.urlsafe_b64encode(private_bytes).decode('ascii').rstrip('=')
    
    print("\n--- NEW VAPID KEYS GENERATED ---\n")
    print(f"VAPID_PUBLIC_KEY={pub_b64}")
    print(f"VAPID_PRIVATE_KEY={priv_b64}")
    print("\nAdd these to your .env file.\n")

if __name__ == "__main__":
    generate_vapid_keys()
