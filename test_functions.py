#!/usr/bin/env python3
import sys
import time
import logging
import traceback

from functions import (
    generate_password, generate_email, generate_ipv4, generate_ipv6,
    generate_mac, generate_url, generate_company, generate_phone,
    generate_name, generate_fullname, generate_sentence,
    generate_credit_card, hash_sha256, hash_bcrypt, encrypt_aes, run_ddos
)

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def test_generate_functions():
    logging.info("Тестируем генерацию данных...")

    try:
        pw = generate_password(16)
        logging.debug(f"Password (16 chars): {pw}")

        email = generate_email()
        logging.debug(f"Email: {email}")

        ipv4 = generate_ipv4()
        logging.debug(f"IPv4 (random): {ipv4}")

        ipv4_mask = generate_ipv4("24")
        logging.debug(f"IPv4 with /24 mask: {ipv4_mask}")

        ipv6 = generate_ipv6()
        logging.debug(f"IPv6: {ipv6}")

        mac = generate_mac()
        logging.debug(f"MAC: {mac}")

        url = generate_url()
        logging.debug(f"URL: {url}")

        company_local = generate_company(local=True)
        company_global = generate_company(local=False)
        logging.debug(f"Company (local): {company_local}")
        logging.debug(f"Company (global): {company_global}")

        phone_local = generate_phone(local=True)
        phone_global = generate_phone(local=False)
        logging.debug(f"Phone (local): {phone_local}")
        logging.debug(f"Phone (global): {phone_global}")

        name_local = generate_name(local=True)
        name_global = generate_name(local=False)
        logging.debug(f"Name (local): {name_local}")
        logging.debug(f"Name (global): {name_global}")

        fullname_local = generate_fullname(local=True)
        fullname_global = generate_fullname(local=False)
        logging.debug(f"Fullname (local): {fullname_local}")
        logging.debug(f"Fullname (global): {fullname_global}")

        sentence_local = generate_sentence(local=True)
        sentence_global = generate_sentence(local=False)
        logging.debug(f"Sentence (local): {sentence_local}")
        logging.debug(f"Sentence (global): {sentence_global}")

        ccard = generate_credit_card()
        logging.debug(f"Credit Card Number: {ccard}")

    except Exception:
        logging.error("Ошибка при генерации данных:\n" + traceback.format_exc())


def test_hash_encrypt():
    logging.info("Тестируем хеширование и шифрование...")

    test_str = "TestString123!@#"
    logging.debug(f"Исходная строка: {test_str}")

    try:
        sha = hash_sha256(test_str)
        logging.debug(f"SHA256: {sha}")
    except Exception:
        logging.error("Ошибка SHA256:\n" + traceback.format_exc())

    try:
        bcrypt_hash = hash_bcrypt(test_str)
        logging.debug(f"bcrypt: {bcrypt_hash}")
    except Exception:
        logging.error("Ошибка bcrypt:\n" + traceback.format_exc())

    try:
        key = "mysecretkey1234567890"
        encrypted = encrypt_aes(test_str, key)
        logging.debug(f"AES зашифровано: {encrypted}")
    except Exception:
        logging.error("Ошибка AES шифрования:\n" + traceback.format_exc())


def test_ddos_short():
    logging.info("Тестируем DDOS-имитацию (короткий тест 3 запроса)...")

    # Для теста — используем localhost и порт 80
    # Реальный запуск на внешний сервер может быть незаконен и нарушать правила.

    import threading
    import requests

    def run_short_ddos():
        try:
            base_url = "http://localhost:80"
            count = 0
            while count < 3:
                t0 = time.time()
                try:
                    resp = requests.get(base_url)
                    dt = time.time() - t0
                    count += 1
                    logging.debug(f"[{count}] Статус: {resp.status_code} за {dt:.3f} сек")
                except Exception as e:
                    logging.error(f"Ошибка запроса: {e}")
                time.sleep(0.1)
            logging.info("DDOS тест завершён успешно.")
        except KeyboardInterrupt:
            logging.info("DDOS тест прерван пользователем.")

    thread = threading.Thread(target=run_short_ddos)
    thread.start()
    thread.join()


if __name__ == "__main__":
    logging.info("=== Запуск тестов functions.py ===")

    test_generate_functions()
    test_hash_encrypt()

    # Раскомментируй, если хочешь протестировать DDOS-имитацию (лучше на локальном сервере!)
    # test_ddos_short()

    logging.info("=== Тесты завершены ===")
