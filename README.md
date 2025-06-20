# faker-utils

A utility for generating fake data and creating test files, with the ability to simulate server load (basic DDoS testing).

---

## Description

`faker-utils` is a Python-based toolkit for generating various types of fake data (passwords, emails, IP addresses, MAC addresses, URLs, companies, phones, and more), as well as utilities for file generation and deletion, and a simple HTTP load testing module.

The project uses the [Faker](https://faker.readthedocs.io/) library with localization support and includes functions for data hashing and AES encryption.

---

## Features

- Fake data generation:
  - Passwords (customizable length)
  - Email addresses
  - IPv4 and IPv6 addresses (with mask for IPv4)
  - MAC addresses
  - URLs
  - Company names, names, full names, sentences
  - Phone numbers (with optional localization)
  - Credit card numbers
- Hashing (SHA256, bcrypt)
- AES encryption with user-provided key
- File generation with controlled count and total size
- Infinite file generation (for disk pressure testing)
- Cleanup of previously created files
- DDoS load simulation via repeated HTTP requests

---

## Installation

It's recommended to use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
Run from terminal:
```bash
./main.py <command> [options]
```
| Command    | Description                                 | Example                                        |
| ---------- | ------------------------------------------- | ---------------------------------------------- |
| `passwd`   | Generate password                           | `./main.py passwd 16 --hash sha256`            |
| `email`    | Generate email address                      | `./main.py email`                              |
| `ipv4`     | Generate IPv4 address (with optional mask)  | `./main.py ipv4 24`                            |
| `ipv6`     | Generate IPv6 address                       | `./main.py ipv6`                               |
| `mac`      | Generate MAC address                        | `./main.py mac`                                |
| `url`      | Generate URL                                | `./main.py url`                                |
| `company`  | Generate company name (localized with `-l`) | `./main.py company -l`                         |
| `phone`    | Generate phone number (localized with `-l`) | `./main.py phone -l`                           |
| `name`     | Generate name (localized with `-l`)         | `./main.py name -l`                            |
| `fullname` | Generate full name (localized with `-l`)    | `./main.py fullname -l`                        |
| `sentence` | Generate sentence (localized with `-l`)     | `./main.py sentence -l`                        |
| `ccard`    | Generate credit card number                 | `./main.py ccard`                              |
| `file`     | Generate files with total size control      | `./main.py file 10 100 /tmp/testfiles`         |
| `infile`   | Infinite file generation (Ctrl+C to stop)   | `./main.py infile /tmp/testfiles`              |
| `clean`    | Clean up generated files                    | `./main.py clean /tmp/testfiles`               |
| `ddos`     | Simulate server load via HTTP requests      | `./main.py ddos example.com 80 --interval 0.1` |

## Hashing and Encryption
- --hash: Supports sha256 and bcrypt
- --encrypt: AES encryption, requires --key

## Testing
A Dockerfile based on Ubuntu 22.04 is included.
To build and run:
```bash
docker build -t faker-utils-test .
docker run --rm faker-utils-test
```

## Use:
The utility is under development. The end-use format is being finalized.
