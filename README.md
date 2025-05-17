# Secure Big Data Processing with RSA Encryption

## Overview

This project serves as a proof of concept for secure big data processing using RSA encryption. It demonstrates how to encrypt sensitive customer information while efficiently processing large datasets with Apache Spark. The goal is to ensure data privacy and security in big data applications.

## Features

- **RSA Encryption**: Implements asymmetric encryption to secure sensitive data such as Social Security Numbers (SSN), first names, last names, and credit card numbers (CCN).
- **Data Processing**: Utilizes PySpark for scalable and efficient handling of large datasets.
- **Sample Data**: Includes a CSV file (`sample-data.csv`) containing customer information for testing and demonstration purposes.
- **Verification**: Provides functionality to decrypt a sample of encrypted data for verification purposes.

## Files Included

- `big_data_security_poc.py`: The main Python script that initializes the Spark session, generates RSA keys, encrypts sensitive fields, processes the data, and displays results.
- `sample-data.csv`: A sample dataset containing customer information used for testing the encryption and processing functionalities.
- `tempCodeRunnerFile.py`: A temporary script that contains similar functionality to `big_data_security_poc.py` for testing purposes.

## Getting Started

### Prerequisites

- Python 3.x
- PySpark
- Pandas
- Cryptography library

### Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
