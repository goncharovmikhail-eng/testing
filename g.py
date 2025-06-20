#!/usr/bin/env python3
import sys
import argparse
import hashlib
import bcrypt
import base64
import random
import ipaddress
from cryptography.fernet import Fernet
from faker import Faker

fake = Faker()
fake_ru = Faker("ru_RU")

# --- Генераторы данных ---

def generate_password(length=12):
    return fake.password(length=length, special_chars=True, digits=True, upper_case=True, lower_case=True)

def generate_email():
    username = fake.user_name()
    domain = fake.domain_name()
    return f"{username}@{domain}"

def generate_ipv4(mask=None):
    private_prefixes = ["10.0.0.0", "172.16.0.0", "192.168.0.0"]
    try:
        if mask:
            if not str(mask).startswith("/"):
                mask = "/" + str(mask)
            base = random.choice(private_prefixes)
            network = ipaddress.IPv4Network(base + mask, strict=False)
            hosts = list(network.hosts())
            if not hosts:
                raise ValueError("Слишком узкая маска — нет доступных адресов.")
            return str(random.choice(hosts))
        else:
            while True:
                ip = ipaddress.IPv4Address(random.randint(1, (2**32) - 1))
                if not ip.is_private and not ip.is_multicast and not ip.is_reserved and not ip.is_loopback:
                    return str(ip)
    except Exception as e:
        print(f"Ошибка: неверная маска {mask}: {e}")
        sys.exit(1)

def generate_ipv6():
    return fake.ipv6()

def generate_mac():
    return fake.mac_address()

def generate_url():
    return fake.url()

def generate_company(local=False):
    return fake_ru.company() if local else fake.company()

def generate_phone(local=False):
    return fake_ru.phone_number() if local else fake.msisdn()

def generate_name(local=False):
    return fake_ru.name() if local else fake.name()

def generate_fullname(local=False):
    return fake_ru.name() if local else fake.name()

def generate_sentence(local=False):
    return fake_ru.sentence() if local else fake.sentence()

def generate_credit_card():
    return fake.credit_card_number(card_type=None)

# --- Хеш-функции ---

def hash_sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

def hash_bcrypt(data):
    return bcrypt.hashpw(data.encode(), bcrypt.gensalt()).decode()

# --- Шифрование ---

def encrypt_aes(data, key):
    key_bytes = key.encode()
    key_32 = base64.urlsafe_b64encode(key_bytes.ljust(32, b'_')[:32])
    cipher = Fernet(key_32)
    return cipher.encrypt(data.encode()).decode()

# --- Обработка вывода ---

def process_output(data, args):
    original = data
    if getattr(args, 'hash', None):
        if args.hash == 'sha256':
            hashed = hash_sha256(original)
        elif args.hash == 'bcrypt':
            hashed = hash_bcrypt(original)
        return f"Исходное значение: {original}\nХеш ({args.hash}): {hashed}"
    elif getattr(args, 'encrypt', None):
        if not getattr(args, 'key', None):
            print("Ошибка: для шифрования нужно указать --key")
            sys.exit(1)
        encrypted = encrypt_aes(original, args.key)
        return f"Исходное значение: {original}\nЗашифровано (AES): {encrypted}"
    return original

# --- Парсер и логика разбора команд ---

def create_main_parser():
    parser = argparse.ArgumentParser(add_help=False)
    subparsers = parser.add_subparsers(dest='command')

    common_opts = {
        "hash": dict(choices=['sha256', 'bcrypt'], help="Хешировать результат"),
        "encrypt": dict(choices=['aes'], help="Зашифровать результат"),
        "key": dict(help="Ключ для шифрования (обязательно при --encrypt)")
    }

    p = subparsers.add_parser('passwd', add_help=False)
    p.add_argument("length", type=int, nargs='?', default=12)
    for k, v in common_opts.items():
        p.add_argument(f"--{k}", **v)

    for name in ['email', 'ipv6', 'mac', 'url']:
        sp = subparsers.add_parser(name, add_help=False)
        for k, v in common_opts.items():
            sp.add_argument(f"--{k}", **v)

    sp = subparsers.add_parser('ipv4', add_help=False)
    sp.add_argument("mask", nargs='?')
    for k, v in common_opts.items():
        sp.add_argument(f"--{k}", **v)

    sp = subparsers.add_parser('phone', add_help=False)
    sp.add_argument("-l", "--local", action="store_true")
    for k, v in common_opts.items():
        sp.add_argument(f"--{k}", **v)

    sp = subparsers.add_parser('name', add_help=False)
    sp.add_argument("-l", "--local", action="store_true")
    for k, v in common_opts.items():
        sp.add_argument(f"--{k}", **v)

    sp = subparsers.add_parser('fullname', add_help=False)
    sp.add_argument("-l", "--local", action="store_true")
    for k, v in common_opts.items():
        sp.add_argument(f"--{k}", **v)

    sp = subparsers.add_parser('sentence', add_help=False)
    sp.add_argument("-l", "--local", action="store_true")
    for k, v in common_opts.items():
        sp.add_argument(f"--{k}", **v)

    sp = subparsers.add_parser('ccard', add_help=False)
    for k, v in common_opts.items():
        sp.add_argument(f"--{k}", **v)

    sp = subparsers.add_parser('company', add_help=False)
    sp.add_argument("-l", "--local", action="store_true")
    for k, v in common_opts.items():
        sp.add_argument(f"--{k}", **v)

    return parser, subparsers

def split_commands(args, command_names):
    """Разбивает список args на подсписки — по командам из command_names"""
    indices = []
    for i, arg in enumerate(args):
        if arg in command_names:
            indices.append(i)
    indices.append(len(args))

    result = []
    for i in range(len(indices) - 1):
        chunk = args[indices[i]:indices[i+1]]
        result.append(chunk)
    return result

def main():
    parser, subparsers = create_main_parser()

    args = sys.argv[1:]
    command_names = subparsers.choices.keys()
    commands = split_commands(args, command_names)

    for cmd_args in commands:
        try:
            parsed = parser.parse_args(cmd_args)
        except SystemExit:
            print(f"Ошибка в команде: {' '.join(cmd_args)}")
            continue

        if parsed.command == "passwd":
            data = generate_password(parsed.length)
        elif parsed.command == "email":
            data = generate_email()
        elif parsed.command == "ipv4":
            data = generate_ipv4(parsed.mask)
        elif parsed.command == "ipv6":
            data = generate_ipv6()
        elif parsed.command == "mac":
            data = generate_mac()
        elif parsed.command == "url":
            data = generate_url()
        elif parsed.command == "company":
            data = generate_company(parsed.local)
        elif parsed.command == "phone":
            data = generate_phone(parsed.local)
        elif parsed.command == "name":
            data = generate_name(parsed.local)
        elif parsed.command == "fullname":
            data = generate_fullname(parsed.local)
        elif parsed.command == "sentence":
            data = generate_sentence(parsed.local)
        elif parsed.command == "ccard":
            data = generate_credit_card()
        else:
            print(f"Неизвестная команда: {parsed.command}")
            continue

        output = process_output(data, parsed)
        print(output)


if __name__ == "__main__":
    main()
