import sys
import random
import ipaddress
import hashlib
import bcrypt
import base64
import time
from cryptography.fernet import Fernet
from faker import Faker
try:
    import requests
except ImportError:
    requests = None

fake = Faker()
fake_ru = Faker("ru_RU")

def generate_password(length=12):
    return fake.password(length=length, special_chars=True, digits=True, upper_case=True, lower_case=True)

def generate_email():
    return f"{fake.user_name()}@{fake.domain_name()}"

def generate_ipv4(mask=None):
    private_prefixes = ["10.0.0.0", "172.16.0.0", "192.168.0.0"]
    try:
        if mask:
            mask = "/" + str(mask).lstrip("/")
            base = random.choice(private_prefixes)
            network = ipaddress.IPv4Network(base + mask, strict=False)
            return str(random.choice(list(network.hosts())))
        else:
            while True:
                ip = ipaddress.IPv4Address(random.randint(1, (2**32) - 1))
                if not ip.is_private and not ip.is_multicast and not ip.is_reserved and not ip.is_loopback:
                    return str(ip)
    except Exception as e:
        sys.exit(f"Ошибка: неверная маска {mask}: {e}")

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

def hash_sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

def hash_bcrypt(data):
    return bcrypt.hashpw(data.encode(), bcrypt.gensalt()).decode()

def encrypt_aes(data, key):
    key_bytes = key.encode()
    key_32 = base64.urlsafe_b64encode(key_bytes.ljust(32, b'_')[:32])
    cipher = Fernet(key_32)
    return cipher.encrypt(data.encode()).decode()

def process_output(data, args):
    original = data
    if getattr(args, 'hash', None):
        hashed = hash_sha256(original) if args.hash == 'sha256' else hash_bcrypt(original)
        return f"Исходное значение: {original}\nХеш ({args.hash}): {hashed}"
    elif getattr(args, 'encrypt', None):
        if not getattr(args, 'key', None):
            sys.exit("Ошибка: для шифрования нужно указать --key")
        encrypted = encrypt_aes(original, args.key)
        return f"Исходное значение: {original}\nЗашифровано (AES): {encrypted}"
    return original

def run_ddos(url: str, port: int, interval: float = 0.1):
    if requests is None:
        print("Ошибка: для ddos требуется установить requests (pip install requests)")
        return

    base_url = f"http://{url}:{port}"
    print(f"Начинаем нагрузку на {base_url}. Ctrl+C для остановки.")
    count = 0
    try:
        while True:
            start = time.time()
            try:
                resp = requests.get(base_url)
                dt = time.time() - start
                count += 1
                print(f"[{count}] {resp.status_code} за {dt:.3f} сек")
            except Exception as e:
                print(f"[{count}] Ошибка запроса: {e}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nНагрузка остановлена.")
