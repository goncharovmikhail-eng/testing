#!/usr/bin/env python3
import argparse
import hashlib
import bcrypt
import base64
import sys
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

# --- Обработка опций ---

def process_output(data, args):
    if args.hash:
        if args.hash == 'sha256':
            data = hash_sha256(data)
        elif args.hash == 'bcrypt':
            data = hash_bcrypt(data)
    elif args.encrypt:
        if not args.key:
            print("Ошибка: для шифрования нужно указать --key")
            sys.exit(1)
        data = encrypt_aes(data, args.key)
    return data

# --- CLI ---

def main():
    parser = argparse.ArgumentParser(description="faker-cli — генерация тестовых данных")
    subparsers = parser.add_subparsers(dest='command')

    common_opts = {
        "hash": dict(choices=['sha256', 'bcrypt'], help="Хешировать результат"),
        "encrypt": dict(choices=['aes'], help="Зашифровать результат"),
        "key": dict(help="Ключ для шифрования (обязательно при --encrypt)")
    }

    # passwd
    p = subparsers.add_parser('passwd', help="Генерация пароля")
    p.add_argument("length", type=int, nargs='?', default=12, help="Длина пароля")
    for k, v in common_opts.items():
        p.add_argument(f"--{k}", **v)

    # команды без параметров
    for name in ['email', 'ipv6', 'mac', 'url']:
        sp = subparsers.add_parser(name, help=f"Генерация {name}")
        for k, v in common_opts.items():
            sp.add_argument(f"--{k}", **v)

    # ipv4
    sp = subparsers.add_parser('ipv4', help="Генерация IPv4-адреса")
    sp.add_argument("mask", nargs='?', help="CIDR-маска (например: /24 или 16)")
    for k, v in common_opts.items():
        sp.add_argument(f"--{k}", **v)

    # phone
    sp = subparsers.add_parser('phone', help="Генерация номера телефона")
    sp.add_argument("-l", "--local", action="store_true", help="Российский номер")
    for k, v in common_opts.items():
        sp.add_argument(f"--{k}", **v)

    # name
    sp = subparsers.add_parser('name', help="Генерация имени")
    sp.add_argument("-l", "--local", action="store_true", help="Русское имя")
    for k, v in common_opts.items():
        sp.add_argument(f"--{k}", **v)

    # fullname
    sp = subparsers.add_parser('fullname', help="Генерация полного имени")
    sp.add_argument("-l", "--local", action="store_true", help="Русское имя")
    for k, v in common_opts.items():
        sp.add_argument(f"--{k}", **v)

    # sentence
    sp = subparsers.add_parser('sentence', help="Генерация случайного предложения")
    sp.add_argument("-l", "--local", action="store_true", help="Русский текст")
    for k, v in common_opts.items():
        sp.add_argument(f"--{k}", **v)

    # ccard
    sp = subparsers.add_parser('ccard', help="Генерация номера кредитной карты")
    for k, v in common_opts.items():
        sp.add_argument(f"--{k}", **v)

    # company
    sp = subparsers.add_parser('company', help="Генерация названия компании")
    sp.add_argument("-l", "--local", action="store_true", help="Русская компания")
    for k, v in common_opts.items():
        sp.add_argument(f"--{k}", **v)

    args = parser.parse_args()

    # Логика выбора генератора
    data = None
    if args.command == "passwd":
        data = generate_password(args.length)
    elif args.command == "email":
        data = generate_email()
    elif args.command == "ipv4":
        data = generate_ipv4(args.mask)
    elif args.command == "ipv6":
        data = generate_ipv6()
    elif args.command == "mac":
        data = generate_mac()
    elif args.command == "url":
        data = generate_url()
    elif args.command == "company":
        data = generate_company(args.local)
    elif args.command == "phone":
        data = generate_phone(args.local)
    elif args.command == "name":
        data = generate_name(args.local)
    elif args.command == "fullname":
        data = generate_fullname(args.local)
    elif args.command == "sentence":
        data = generate_sentence(args.local)
    elif args.command == "ccard":
        data = generate_credit_card()
    else:
        parser.print_help()
        sys.exit(1)

    print(process_output(data, args))

if __name__ == "__main__":
    main()

