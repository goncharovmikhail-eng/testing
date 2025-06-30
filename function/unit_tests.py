#!/usr/bin/env python3
import unittest
from passwd_gen import PasswordGenerator

class TestPasswordGenerator(unittest.TestCase):
    def setUp(self):
        self.min_len = 8
        self.max_len = 16
        self.gen = PasswordGenerator(self.min_len, self.max_len)

    def test_valid_password_min_length(self):
        pwd = self.gen.valid_password_min_length()
        print(f"[DEBUG] valid_password_min_length: '{pwd}' length={len(pwd)}")
        self.assertIsInstance(pwd, str)
        self.assertGreaterEqual(len(pwd), self.min_len)
        self.assertLessEqual(len(pwd), self.max_len)

    def test_valid_password_max_length_lowercase(self):
        pwd = self.gen.valid_password_max_length_lowercase()
        print(f"[DEBUG] valid_password_max_length_lowercase: '{pwd}' length={len(pwd)}")
        self.assertTrue(all(c.islower() for c in pwd))
        self.assertEqual(len(pwd), self.max_len)

    def test_valid_password_mid_length_digits(self):
        pwd = self.gen.valid_password_mid_length_digits()
        mid = (self.min_len + self.max_len) // 2
        print(f"[DEBUG] valid_password_mid_length_digits: '{pwd}' length={len(pwd)}")
        self.assertTrue(all(c.isdigit() for c in pwd))
        self.assertEqual(len(pwd), mid)

    def test_valid_password_mid_length_specials(self):
        pwd = self.gen.valid_password_mid_length_specials()
        mid = (self.min_len + self.max_len) // 2
        allowed = set(self.gen.specials)
        print(f"[DEBUG] valid_password_mid_length_specials: '{pwd}' length={len(pwd)}")
        self.assertTrue(all(c in allowed for c in pwd))
        self.assertEqual(len(pwd), mid)

    def test_invalid_password_too_short(self):
        pwd = self.gen.invalid_password_too_short()
        print(f"[DEBUG] invalid_password_too_short: '{pwd}' length={len(pwd)}")
        self.assertTrue(len(pwd) < self.min_len)

    def test_invalid_password_too_long(self):
        pwd = self.gen.invalid_password_too_long()
        print(f"[DEBUG] invalid_password_too_long: '{pwd}' length={len(pwd)}")
        self.assertTrue(len(pwd) > self.max_len)

    def test_invalid_password_empty(self):
        pwd = self.gen.invalid_password_empty()
        print(f"[DEBUG] invalid_password_empty: '{pwd}' length={len(pwd)}")
        self.assertEqual(pwd, "")

    def test_invalid_password_with_cyrillic(self):
        pwd = self.gen.invalid_password_with_cyrillic()
        cyrillic_set = set(self.gen.cyrillic)
        print(f"[DEBUG] invalid_password_with_cyrillic: '{pwd}' length={len(pwd)}")
        self.assertTrue(any(c in cyrillic_set for c in pwd))

    def test_invalid_non_string_samples(self):
        samples = self.gen.invalid_non_string_samples()
        print(f"[DEBUG] invalid_non_string_samples: {samples}")
        for s in samples:
            self.assertFalse(isinstance(s, str))

    def test_generate_valid_passwords_count(self):
        count = 2
        pwds = self.gen.generate_valid_passwords(count)
        print(f"[DEBUG] generate_valid_passwords_count: count={count} total_passwords={len(pwds)}")
        self.assertEqual(len(pwds), 4 * count)

    def test_generate_invalid_passwords_count(self):
        count = 2
        pwds = self.gen.generate_invalid_passwords(count)
        expected_min = 4 * count + 6 * count
        print(f"[DEBUG] generate_invalid_passwords_count: count={count} total_passwords={len(pwds)} expected_min={expected_min}")
        self.assertGreaterEqual(len(pwds), expected_min)

if __name__ == '__main__':
    unittest.main()

