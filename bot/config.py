# -*- coding: utf-8 -*-

import os
import logging
import sys

debug = int(os.getenv('DEBUG', 1))

if debug:
    token = os.getenv('DEBUG_TOKEN')
else:
    token = os.getenv('PROD_TOKEN')

user_token = os.getenv('USER_TOKEN')
godville_token = os.getenv('GODVILLE_TOKEN')

godville_url = f'https://godville.net/gods/api/%D0%9A%D1%80%D0%BE%D0%BB%D0%BB/{godville_token}'

my_id = [181535096, 145895954]   # Основной и дебаг паблики соответственно
my_id = my_id[debug]

creator_id = 35518049

workersneeded = 3 if debug else 8

reminder_sleeps = 30
vk_groupchats_id_limit = int(2e9)


# Create a logger
logger = logging.getLogger('LOG')
if not logger.hasHandlers():
    logger.setLevel(logging.DEBUG)

    # Create handlers
    c_handler = logging.StreamHandler(sys.stdout)
    f_handler = logging.FileHandler('logs/last.log', mode='w', encoding='utf-8')

    c_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    f_handler.setLevel(logging.WARNING)

    # Create formatters and add it to handlers
    log_format = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(log_format)
    f_handler.setFormatter(log_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
