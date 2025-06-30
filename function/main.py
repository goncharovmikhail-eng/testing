#!/usr/bin/env python3
import argparse
from password_generator import PasswordGenerator


def main():
    parser = argparse.ArgumentParser(description="Генератор паролей")

    parser.add_argument(
        '-l', '--length', type=int, default=12,
        help='Длина пароля (по умолчанию 12)'
    )
    parser.add_argument(
        '-v', '--valid', type=int, default=0, metavar='N',
        help='Количество валидных паролей для генерации (по умолчанию 0)'
    )
    parser.add_argument(
        '-i', '--invalid', type=int, default=0, metavar='N',
        help='Количество невалидных паролей для генерации (по умолчанию 0)'
    )

    args = parser.parse_args()

    if args.length <= 0:
        parser.error("Длина пароля должна быть положительной")
    if args.valid < 0 or args.invalid < 0:
        parser.error("Количество паролей не может быть отрицательным")

    total_valid = args.valid
    total_invalid = args.invalid

    # Если ни валидных, ни невалидных не указано — генерируем 1 валидный по умолчанию
    if total_valid == 0 and total_invalid == 0:
        total_valid = 1

    gen = PasswordGenerator(min_length=args.length, max_length=args.length)

    if total_valid > 0:
        print(f"Генерируем {total_valid} валидных паролей длиной {args.length}:")
        valid_pwds = gen.generate_valid_passwords(total_valid)
        for pwd in valid_pwds:
            print("  ", pwd)

    if total_invalid > 0:
        print(f"\nГенерируем {total_invalid} невалидных паролей:")
        invalid_pwds = gen.generate_invalid_passwords(total_invalid)
        for pwd in invalid_pwds:
            print("  ", pwd)

if __name__ == "__main__":
    main()
