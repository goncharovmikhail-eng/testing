#!/usr/bin/env python3
import random
import string
from typing import List, Tuple

class PasswordGenerator:
    def __init__(self, min_length: int = 12, max_length: int = 12):
        self.min_length = min_length
        self.max_length = max_length
        self.digits = string.digits
        self.lowers = string.ascii_lowercase
        self.uppers = string.ascii_uppercase
        self.specials = "!@#$%^&*()"
        self.cyrillic = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

    def random_password(self, length: int, chars: str) -> str:
        return ''.join(random.choice(chars) for _ in range(length))

    # Валидные классы паролей
    def valid_password_min_length(self) -> str:
        return self.random_password(self.min_length, self.digits + self.lowers + self.uppers + self.specials)

    def valid_password_max_length_lowercase(self) -> str:
        return self.random_password(self.max_length, self.lowers)

    def valid_password_mid_length_digits(self) -> str:
        mid = (self.min_length + self.max_length) // 2
        return self.random_password(mid, self.digits)

    def valid_password_mid_length_specials(self) -> str:
        mid = (self.min_length + self.max_length) // 2
        return self.random_password(mid, self.specials)

    # Невалидные классы паролей
    def invalid_password_too_short(self) -> str:
        length = random.randint(1, max(1, self.min_length - 1))
        return self.random_password(length, self.digits + self.lowers + self.uppers + self.specials)

    def invalid_password_too_long(self) -> str:
        length = random.randint(self.max_length + 1, self.max_length + 20)
        return self.random_password(length, self.digits + self.lowers + self.uppers + self.specials)

    def invalid_password_empty(self) -> str:
        return ""

    def invalid_password_with_cyrillic(self) -> str:
        length = random.randint(self.min_length, self.max_length)
        return self.random_password(length, self.lowers + self.cyrillic)

    def invalid_non_string_samples(self) -> List:
        return [123456, None, [], ["password"], {}, 12.34]

    # Генерация списков паролей
    def generate_valid_passwords(self, count_per_class: int) -> List[str]:
        valid_funcs = [
            self.valid_password_min_length,
            self.valid_password_max_length_lowercase,
            self.valid_password_mid_length_digits,
            self.valid_password_mid_length_specials,
        ]
        passwords = []
        for func in valid_funcs:
            for _ in range(count_per_class):
                passwords.append(func())
        return passwords

    def generate_invalid_passwords(self, count_per_class: int) -> List:
        invalid_funcs = [
            self.invalid_password_too_short,
            self.invalid_password_too_long,
            self.invalid_password_empty,
            self.invalid_password_with_cyrillic,
        ]
        passwords = []
        for func in invalid_funcs:
            for _ in range(count_per_class):
                passwords.append(func())
        # Добавим нестроковые значения (повторим по количеству count_per_class)
        passwords.extend(self.invalid_non_string_samples() * count_per_class)
        return passwords
def run_simple_mode(args):
    # Если нет аргументов, просто 1 валидный длиной 12
    if args.valid == 0 and args.invalid == 0 and args.count is None:
        gen = PasswordGenerator(min_length=12, max_length=12)
        pwds = gen.generate_valid_passwords(1)
        print(*pwds, sep='\n')
        return

    # Если указаны -v и -i и -c
    # Вычисляем сколько валидных и невалидных паролей в итоге сгенерить
    total_count = args.count if args.count is not None else 1
    valid_count = args.valid if args.valid is not None else 0
    invalid_count = args.invalid if args.invalid is not None else 0

    # Например, если указаны valid=5, invalid=3, count=10 — надо проверить на консистентность
    if valid_count + invalid_count > total_count:
        print("Ошибка: сумма валидных и невалидных паролей не может превышать общее количество.")
        return

    gen = PasswordGenerator(min_length=args.length, max_length=args.length)

    if valid_count > 0:
        print(f"Генерируем {valid_count} валидных паролей:")
        valid_pwds = gen.generate_valid_passwords(valid_count)
        print(*valid_pwds, sep='\n')

    if invalid_count > 0:
        print(f"\nГенерируем {invalid_count} невалидных паролей:")
        invalid_pwds = gen.generate_invalid_passwords(invalid_count)
        print(*invalid_pwds, sep='\n')

