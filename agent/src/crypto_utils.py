import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.exceptions import InvalidTag

class CryptoManager:
    """
    Handles all cryptographic operations including key exchange (X25519) 
    and symmetric encryption (AES-256-GCM).
    """
    
    @staticmethod
    def generate_ephemeral_keypair():
        """Generates an X25519 key pair for a single session."""
        private_key = x25519.X25519PrivateKey.generate()
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def derive_session_key(private_key: x25519.X25519PrivateKey, peer_public_key_bytes: bytes) -> bytes:
        """
        Performs Diffie-Hellman exchange and derives a 32-byte AES key using HKDF.
        """
        peer_public_key = x25519.X25519PublicKey.from_public_bytes(peer_public_key_bytes)
        shared_secret = private_key.exchange(peer_public_key)
        
        # HKDF to ensure the key is uniformly distributed and tied to the application context
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"decentralized-data-syndicate-session-key",
        ).derive(shared_secret)
        
        return derived_key

    @staticmethod
    def encrypt_payload(key: bytes, plaintext: bytes, associated_data: bytes = b"") -> bytes:
        """
        Encrypts data using AES-GCM. 
        Returns nonce + ciphertext + tag combined.
        """
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)  # Standard 96-bit nonce for GCM
        ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
        return nonce + ciphertext

    @staticmethod
    def decrypt_payload(key: bytes, encrypted_blob: bytes, associated_data: bytes = b"") -> bytes:
        """
        Decrypts data using AES-GCM.
        """
        if len(encrypted_blob) < 12:
            raise ValueError("Encrypted blob too short to contain nonce")
            
        nonce = encrypted_blob[:12]
        ciphertext = encrypted_blob[12:]
        
        aesgcm = AESGCM(key)
        try:
            return aesgcm.decrypt(nonce, ciphertext, associated_data)
        except InvalidTag:
            raise ValueError("Decryption failed: Invalid tag or corrupted data")
