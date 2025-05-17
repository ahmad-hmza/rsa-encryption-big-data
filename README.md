# Secure Data Processing with Apache Spark and RSA Encryption

## Introduction

Big data environments process massive datasets across distributed systems, making data confidentiality a critical concern. Apache Spark, a powerful framework for distributed data processing, handles large-scale data efficiently but lacks built-in mechanisms to secure sensitive information during computation. RSA, an asymmetric encryption algorithm, uses a public key for encryption and a private key for decryption, offering secure data protection without the need to share secret keys across nodes. 

This project demonstrates secure data processing using Apache Spark and RSA encryption, processing a dataset of 30 customer records, encrypting sensitive fields (Social Security Number, first name, last name, and credit card number), and counting customers per state while keeping sensitive data confidential.

## Problem Statement

In big data systems, sensitive personally identifiable information (PII), such as Social Security Numbers (SSNs) and credit card numbers, is processed across distributed nodes, increasing the risk of unauthorized access or data breaches. Without encryption, sensitive fields are exposed during Spark’s distributed computations, potentially compromising confidentiality. 

The challenge is to design a system that processes large datasets efficiently while ensuring sensitive data remains confidential. This project uses RSA to encrypt sensitive fields (SSN, first name, last name, and credit card number) before processing in Spark, ensuring secure data handling in a distributed environment.

## Design

The system integrates RSA encryption with Spark’s distributed processing to ensure data confidentiality. The key components are:

- **Data Source**: A CSV dataset (`sample-data.csv`) containing 30 customer records with fields such as SSN, first name, last name, CCN, and state.
- **RSA Encryption Module**: Uses the cryptography library to generate a 2048-bit RSA key pair and encrypt sensitive fields (SSN, first name, last name, CCN) with the public key before processing.
- **Spark Processing**: Apache Spark performs distributed aggregation, counting the number of customers per state.
- **Decryption Module**: Decrypts sample encrypted fields using the private key to verify the encryption process.

## Workflow

The system follows a structured workflow to ensure secure data processing while maintaining the confidentiality of sensitive fields. The steps are:

1. **Data Ingestion**: Read the `sample-data.csv` file into a Pandas DataFrame, containing 30 customer records with fields including SSN, first name, last name, CCN, and state.
2. **RSA Key Generation**: Generate a 2048-bit RSA key pair using the cryptography library, producing a public key for encryption and a private key for decryption.
3. **Encryption of Sensitive Fields**: Encrypt the SSN, first name, last name, and CCN fields for each record using the RSA public key with OAEP padding. Encode the resulting ciphertexts as base64 strings for compatibility with Spark.
4. **Data Preparation for Spark**: Create a Spark DataFrame containing the encrypted fields and the non-sensitive state field, excluding unencrypted sensitive fields to prevent exposure.
5. **Distributed Processing**: Use Apache Spark to group the data by state and count the number of customers per state, leveraging Spark’s distributed computing capabilities.
6. **Result Collection**: Collect the aggregation results (customer counts per state) from Spark, which are based on the non-encrypted state field.
7. **Verification through Decryption**: Decrypt a sample of encrypted fields (e.g., SSN, first name, last name, CCN) using the RSA private key to verify the integrity and correctness of the encryption process.
8. **Output**: Display the customer counts per state and the decrypted sample to confirm the system’s functionality.

The workflow is visually represented in the accompanying documentation, illustrating the sequence of operations from data ingestion to result output, highlighting the encryption and processing stages.

## Implementation

The project is implemented in Python using Apache Spark and the cryptography library. The key steps are:

1. **Setup**: Initialize a Spark session and generate a 2048-bit RSA key pair.
2. **Data Preparation**: Read the `sample-data.csv` file into a Pandas DataFrame. Encrypt the SSN, first name, last name, and CCN fields using the RSA public key and load the encrypted data into a Spark DataFrame, excluding unencrypted sensitive fields.
3. **Processing**: Use Spark to group the data by state and count the number of customers, simulating a big data aggregation task.
4. **Decryption**: Decrypt a sample of encrypted fields using the private key to verify the encryption/decryption process.

### Code Snippet

Here’s a brief code snippet illustrating the encryption and Spark processing:

```python
# RSA encryption
def rsa_encrypt(data, public_key):
    ciphertext = public_key.encrypt(
        str(data).encode(),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return base64.b64encode(ciphertext).decode()

# Spark aggregation
result = sdf.groupBy("state").count().collect()
