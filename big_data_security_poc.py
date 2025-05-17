from pyspark.sql import SparkSession
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import pandas as pd
import base64
import os

# Initialize Spark session
spark = SparkSession.builder.appName("SecureBigDataProcessingRSA").getOrCreate()

# Generate RSA key pair
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Functions for RSA encryption and decryption
def rsa_encrypt(data, public_key):
    if pd.isna(data):
        return None
    ciphertext = public_key.encrypt(
        str(data).encode(),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return base64.b64encode(ciphertext).decode()  # Encode to string for Spark compatibility

def rsa_decrypt(ciphertext, private_key):
    if ciphertext is None:
        return None
    decoded_ciphertext = base64.b64decode(ciphertext)
    plaintext = private_key.decrypt(
        decoded_ciphertext,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return plaintext.decode()

# Read the CSV file into a Pandas DataFrame
csv_file = "sample-data.csv"
pdf = pd.read_csv(csv_file)

# Encrypt sensitive fields (SSN, first name, last name, CCN)
pdf["encrypted_ssn"] = pdf["SSN"].apply(lambda x: rsa_encrypt(x, public_key))
pdf["encrypted_first_name"] = pdf["first name"].apply(lambda x: rsa_encrypt(x, public_key))
pdf["encrypted_last_name"] = pdf["last name"].apply(lambda x: rsa_encrypt(x, public_key))
pdf["encrypted_ccn"] = pdf["CCN"].apply(lambda x: rsa_encrypt(x, public_key))

# Create Spark DataFrame with encrypted fields and state, excluding original sensitive fields
sdf = spark.createDataFrame(pdf[["encrypted_ssn", "encrypted_first_name", "encrypted_last_name", "encrypted_ccn", "state"]])

# Process data: Count customers per state
result = sdf.groupBy("state").count().collect()

# Display results (no decryption needed for state, as it wasn't encrypted)
print("Customers per State:")
for row in result:
    print(f"{row['state']}: {row['count']} customers")

# Example: Decrypt a sample of encrypted data for verification
sample_encrypted_data = pdf[["encrypted_ssn", "encrypted_first_name", "encrypted_last_name", "encrypted_ccn"]].head(5).to_dict('records')
print("\nSample Decrypted Data (for verification):")
for record in sample_encrypted_data:
    decrypted_ssn = rsa_decrypt(record["encrypted_ssn"], private_key)
    decrypted_first_name = rsa_decrypt(record["encrypted_first_name"], private_key)
    decrypted_last_name = rsa_decrypt(record["encrypted_last_name"], private_key)
    decrypted_ccn = rsa_decrypt(record["encrypted_ccn"], private_key)
    print(f"SSN: {decrypted_ssn}, First Name: {decrypted_first_name}, Last Name: {decrypted_last_name}, CCN: {decrypted_ccn}")

# Clean up Spark session
spark.stop()