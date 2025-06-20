import unittest
import subprocess
import re

class TestGpy(unittest.TestCase):
    SCRIPT = "./g.py"  # Путь к твоему скрипту, при необходимости исправь

    def run_cmd(self, *args):
        """Запускает скрипт с аргументами, возвращает stdout как строку"""
        result = subprocess.run([self.SCRIPT, *args], capture_output=True, text=True)
        return result.stdout.strip()

    def test_passwd_default_length(self):
        output = self.run_cmd("passwd")
        # Проверяем что сгенерирован пароль длиной примерно 12 символов
        # Т.к. вывод может быть либо просто пароль, либо с "Исходное значение:"
        passwd = output.split('\n')[0].replace("Исходное значение: ", "")
        self.assertTrue(8 <= len(passwd) <= 20, f"Password length unexpected: {passwd}")

    def test_passwd_length_16(self):
        output = self.run_cmd("passwd", "16")
        passwd = output.split('\n')[0].replace("Исходное значение: ", "")
        self.assertTrue(len(passwd) == 16)

    def test_email_format(self):
        output = self.run_cmd("email")
        email = output.split('\n')[0].replace("Исходное значение: ", "")
        self.assertRegex(email, r"^[\w\.-]+@[\w\.-]+\.\w+$")

    def test_ipv4_with_mask(self):
        output = self.run_cmd("ipv4", "/24")
        ip = output.split('\n')[0].replace("Исходное значение: ", "")
        # Проверим, что ip корректный IPv4
        octets = ip.split('.')
        self.assertEqual(len(octets), 4)
        for o in octets:
            self.assertTrue(0 <= int(o) <= 255)

    def test_hash_sha256(self):
        output = self.run_cmd("passwd", "--hash", "sha256")
        self.assertIn("Хеш (sha256):", output)
        lines = output.split('\n')
        self.assertEqual(len(lines), 2)
        hashed = lines[1].split(": ")[1]
        # Проверим, что хеш в 64 символа hex
        self.assertRegex(hashed, r"^[0-9a-f]{64}$")

    def test_encrypt_aes_missing_key(self):
        # Шифрование без ключа — должен выйти с ошибкой (код 1)
        proc = subprocess.run([self.SCRIPT, "passwd", "--encrypt", "aes"], capture_output=True, text=True)
        self.assertIn("Ошибка: для шифрования нужно указать --key", proc.stdout)

    def test_encrypt_aes_with_key(self):
        output = self.run_cmd("passwd", "--encrypt", "aes", "--key", "secretkey")
        self.assertIn("Зашифровано (AES):", output)

    def test_multiple_commands(self):
        output = self.run_cmd("passwd", "8", "email", "ipv4", "/24", "--hash", "sha256")
        # В выводе три блока (один на команду)
        # Последняя команда с хешем sha256
        self.assertIn("Хеш (sha256):", output)
        self.assertIn("@", output)  # email есть
        # Проверка, что пароль с длиной 8 есть где-то в выводе
        self.assertTrue(any(len(line.strip()) == 8 for line in output.splitlines()))

if __name__ == "__main__":
    unittest.main()
