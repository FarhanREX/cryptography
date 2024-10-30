# DES-CTR Encryption and Decryption

This Python project implements the DES (Data Encryption Standard) algorithm in CTR (Counter) mode for encryption and decryption of plaintext messages. DES-CTR is not a native mode in the `pycryptodome` library, so this code manually constructs it using a counter that is initialized with a nonce and IV.

## Features

- Encrypts plaintext using DES in CTR mode.
- Decrypts ciphertext back to the original plaintext.
- Uses a nonce and IV to ensure unique counter values for each encryption.
- Implements block-by-block processing with a manually incremented counter.

## How It Works

In CTR mode:
- A unique counter is generated for each block by concatenating a nonce and IV with a counter.
- The counter is encrypted with DES in ECB mode.
- Each encrypted counter is XORed with the plaintext to produce the ciphertext.
- For decryption, the same process is repeated in reverse.

## Prerequisites

- **Python 3.x**
- **pycryptodome Library**: Install using:
  ```bash
  pip install pycryptodome
