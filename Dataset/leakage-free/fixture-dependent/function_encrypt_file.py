import os
from cryptography.fernet import Fernet


def encrypt_file(source_file, destination_file, encryption_key):
    if not os.path.exists(source_file):
        raise FileNotFoundError(f"Error: The source file cannot be found: {source_file}")

    try:
        with open(source_file, 'rb') as f:
            data = f.read()

        f = Fernet(encryption_key)
        encrypted_data = f.encrypt(data)

        with open(destination_file, 'wb') as f:
            f.write(encrypted_data)

        print(f"file '{source_file}' Successfully encrypted and saved to '{destination_file}'。")


    except Exception as e:
        raise Exception(e)
