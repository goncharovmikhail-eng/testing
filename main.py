#!/usr/bin/env python3
import sys
import os
import time
import argparse
from header import *
from functions import *

def add_common_args(parser):
    parser.add_argument("--hash", choices=['sha256', 'bcrypt'])
    parser.add_argument("--encrypt", choices=['aes'])
    parser.add_argument("--key")

def add_file_subparser(subparsers):
    file_parser = subparsers.add_parser("file", help="Генерация файлов для засорения")
    file_parser.add_argument("count", type=int, help="Количество файлов")
    file_parser.add_argument("total_size_mb", type=int, help="Общий размер файлов в мегабайтах")
    file_parser.add_argument("path", help="Путь для сохранения файлов")

def add_other_subparsers(subparsers):
    # Добавляем остальные команды faker
    p = subparsers.add_parser('passwd')
    p.add_argument("length", type=int, nargs='?', default=12)
    add_common_args(p)

    for name in ['email', 'ipv6', 'mac', 'url']:
        sp = subparsers.add_parser(name)
        add_common_args(sp)

    sp_ipv4 = subparsers.add_parser('ipv4')
    sp_ipv4.add_argument("mask", nargs='?')
    add_common_args(sp_ipv4)

    for name in ['phone', 'name', 'fullname', 'sentence', 'company']:
        sp = subparsers.add_parser(name)
        sp.add_argument("-l", "--local", action="store_true")
        add_common_args(sp)

    sp = subparsers.add_parser('ccard')
    add_common_args(sp)

    infile_parser = subparsers.add_parser("infile")
    infile_parser.add_argument("path")

    clean_parser = subparsers.add_parser("clean")
    clean_parser.add_argument("path")

def handle_file_command(args):
    path = os.path.abspath(args.path)
    os.makedirs(path, exist_ok=True)
    size = (args.total_size_mb * 1024 * 1024) // args.count
    for i in range(args.count):
        fname = os.path.join(path, f"gfile_{i}.bin")
        with open(fname, "wb") as f:
            f.write(os.urandom(size))
    print(f"Создано {args.count} файлов общей размер {args.total_size_mb} MB в {path}")

def handle_infile_command(args):
    path = os.path.abspath(args.path)
    os.makedirs(path, exist_ok=True)
    i = 0
    try:
        while True:
            fname = os.path.join(path, f"gfile_{i}.bin")
            with open(fname, "wb") as f:
                f.write(os.urandom(1024*1024))  # 1MB
            print("Создан", fname)
            i += 1
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nПрервано.")

def handle_clean_command(args):
    path = os.path.abspath(args.path)
    deleted = 0
    for f in os.listdir(path):
        if f.startswith("gfile_") and f.endswith(".bin"):
            try:
                os.remove(os.path.join(path, f))
                deleted += 1
            except Exception:
                pass
    print("Удалено файлов:", deleted)

def main():
    parser = argparse.ArgumentParser(description="faker-utils with file generation")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_other_subparsers(subparsers)
    add_file_subparser(subparsers)

    ddos_parser = subparsers.add_parser("ddos", help="Имитация нагрузки на сервер")
    ddos_parser.add_argument("url", help="URL или IP для нагрузки")
    ddos_parser.add_argument("port", type=int, help="Порт для нагрузки")
    ddos_parser.add_argument("--interval", type=float, default=0.1, help="Интервал между запросами")

    args = parser.parse_args()

    if args.command == "file":
        handle_file_command(args)
    elif args.command == "infile":
        handle_infile_command(args)
    elif args.command == "clean":
        handle_clean_command(args)
    elif args.command == "ddos":
        run_ddos(args.url, args.port, args.interval)
    else:
        mapping = {
            "passwd": generate_password,
            "email": generate_email,
            "ipv4": generate_ipv4,
            "ipv6": generate_ipv6,
            "mac": generate_mac,
            "url": generate_url,
            "company": generate_company,
            "phone": generate_phone,
            "name": generate_name,
            "fullname": generate_fullname,
            "sentence": generate_sentence,
            "ccard": generate_credit_card
        }

        func = mapping.get(args.command)
        if not func:
            print(f"Неизвестная команда: {args.command}")
            sys.exit(1)

        if args.command == "passwd":
            data = func(args.length)
        elif args.command == "ipv4":
            data = func(args.mask)
        elif args.command in ("company", "phone", "name", "fullname", "sentence"):
            data = func(getattr(args, "local", False))
        else:
            data = func()

        print(process_output(data, args))


if __name__ == "__main__":
    main()
