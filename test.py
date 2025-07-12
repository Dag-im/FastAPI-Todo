#!/usr/bin/env python3
from dotenv import load_dotenv
import os

# 1) Load .env from the same directory as this script
#    You can pass override=True to ensure it replaces any existing env vars
load_dotenv(override=True)

# 2) Now import Settings (which will pick up the freshly loaded env)
from core.config import Settings

import smtplib

print("HOST:", Settings.EMAIL_HOST)
print("PORT:", Settings.EMAIL_PORT)
print("USER:", Settings.EMAIL_USER)
print("PASS:", Settings.EMAIL_PASSWORD[:4] + "…")

# 3) Test SMTP
server = smtplib.SMTP(Settings.EMAIL_HOST, Settings.EMAIL_PORT, timeout=10)
server.set_debuglevel(1)
server.starttls()
server.login(Settings.EMAIL_USER, Settings.EMAIL_PASSWORD)
print("Logged in successfully!")
server.quit()
