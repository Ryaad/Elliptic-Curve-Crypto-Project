import random
import secrets

# Define a simple elliptic curve y^2 = x^3 + ax + b over a finite field Fp
class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a  # Coefficient a in the equation
        self.b = b  # Coefficient b in the equation
        self.p = p  # Prime number defining the finite field

    def is_on_curve(self, x, y):
        """Check if a point (x, y) is on the curve."""
        return (y**2 - (x**3 + self.a * x + self.b)) % self.p == 0

    def point_addition(self, P, Q):
        """Add two points P and Q on the elliptic curve."""
        if P == (None, None):
            return Q
        if Q == (None, None):
            return P

        x1, y1 = P
        x2, y2 = Q

        if x1 == x2:
            # Point doubling
            m = (3 * x1**2 + self.a) * pow(2 * y1, -1, self.p) % self.p
        else:
            # General addition
            m = (y2 - y1) * pow(x2 - x1, -1, self.p) % self.p

        x3 = (m**2 - x1 - x2) % self.p
        y3 = (m * (x1 - x3) - y1) % self.p

        return (x3, y3)

    def scalar_multiplication(self, k, P):
        """Multiply a point P by an integer k on the elliptic curve."""
        R = (None, None)  # Point at infinity
        for _ in range(k):
            R = self.point_addition(R, P)  # Ajouter P à R à chaque itération

        return R

# Define the elliptic curve parameters
curve = EllipticCurve(a=2, b=3, p=97)                 
# P is too small here and should be like P-256 or P-384
# a and b should be chosen carefully because if not it may simplify the attacks because of some symetries or addition may not be working
                                                

# Define a generator point on the curve
G = (3, 6)   
# The point have to be on the curve of course
if not curve.is_on_curve(G[0], G[1]):
    print("Error: Generator point is not on the curve.")
    exit()  # Arrête l'exécution du programme


# Key generation for two parties
def generate_keypair():
    while True:
        #private_key = random.randint(1, curve.p - 1)  # The random library is weak in cryptography
        private_key = secrets.randbelow(curve.p - 1) + 1
        public_key = curve.scalar_multiplication(private_key, G)
        if public_key != (None, None):  # Ensure valid public key
            return private_key, public_key

# Create the shared key 
def create_shared_key(private_key, peer_public_key):
    shared_key = curve.scalar_multiplication(private_key, peer_public_key)
    return shared_key

# Simple encryption for the example
def encrypt_message(shared_key, message):
    key = shared_key[0]  # Use x-coordinate of the shared key
    return bytes([b ^ key for b in message])

def decrypt_message(shared_key, ciphertext):
    return encrypt_message(shared_key, ciphertext) 

# Demo
def demo():
    print("-------------- ECC Encryption Demo --------------------------")

    # Key generation for Alice and Bob
    alice_private_key, alice_public_key = generate_keypair()
    bob_private_key, bob_public_key = generate_keypair()

    print("Alice's Public Key:", alice_public_key)
    print("Bob's Public Key:", bob_public_key)

    # create shared keys
    alice_shared_key = create_shared_key(alice_private_key, bob_public_key)
    bob_shared_key = create_shared_key(bob_private_key, alice_public_key)

    if alice_shared_key != bob_shared_key:
        print("Shared keys do not match!")
        exit()  
    print("Shared Key:", alice_shared_key)

    # Encrypt and decrypt a message
    message = b"This is a private message that no one should ever read!"
    print("Original Message:", message)

    ciphertext = encrypt_message(alice_shared_key, message)
    print("Ciphertext:", ciphertext)

    decrypted_message = decrypt_message(bob_shared_key, ciphertext)
    print("Decrypted Message:", decrypted_message)

# Run the demo
demo()
