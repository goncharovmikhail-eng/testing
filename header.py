#!/usr/bin/env python3

import sys
import os
import random
import time
import ipaddress
import hashlib
import bcrypt
import base64
import argparse
from cryptography.fernet import Fernet
from faker import Faker

fake = Faker()
fake_ru = Faker("ru_RU")
