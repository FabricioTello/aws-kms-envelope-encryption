# AWS KMS Envelope Encryption

Este proyecto demuestra el funcionamiento del cifrado en sobre (Envelope Encryption) utilizando AWS Key Management Service (KMS) y Python.

## Objetivo

Implementar un ejemplo práctico donde AWS KMS genera y protege una clave de datos, mientras que Python utiliza esa clave para cifrar información mediante AES-256-GCM.

## Tecnologías utilizadas

- AWS Key Management Service (KMS)
- AWS CloudShell
- Python 3
- Boto3
- Cryptography
- AES-256-GCM
- GitHub

## Funcionamiento

El proceso de cifrado funciona de la siguiente manera:

1. Python se conecta con AWS KMS mediante Boto3.
2. KMS genera una clave de datos AES-256 mediante `GenerateDataKey`.
3. KMS devuelve dos versiones de la clave:
   - Plaintext: utilizada temporalmente para cifrar el mensaje.
   - CiphertextBlob: versión cifrada de la clave.
4. Python utiliza la clave en plaintext con AES-GCM para cifrar el mensaje.
5. La clave plaintext deja de utilizarse después del cifrado.
6. En `sobre.json` se almacenan:
   - La clave de datos cifrada.
   - El nonce.
   - El mensaje cifrado.
7. Para descifrar el mensaje, AWS KMS recupera la clave de datos mediante `Decrypt`.
8. Con la clave recuperada, AES-GCM descifra el mensaje original.

## Arquitectura

Mensaje original
      |
      v
AWS KMS -> GenerateDataKey
      |
      v
Clave AES-256
      |
      v
AES-GCM -> Cifrado del mensaje
      |
      v
sobre.json
      |
      v
AWS KMS -> Decrypt
      |
      v
AES-GCM -> Mensaje original

## Archivos

### kms.py

Contiene la lógica para generar la clave de datos mediante AWS KMS, cifrar el mensaje y posteriormente descifrarlo.

### sobre.json

Contiene el resultado del cifrado. La clave AES utilizada para proteger el mensaje no se almacena directamente en texto plano.

## Ejecución

Para ejecutar el programa:

```bash
python3 kms.py
