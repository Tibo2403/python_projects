import os

# Set these environment variables before running (use a Gmail App Password, not your account password)
config_email = os.environ["EMAIL_ADDRESS"]
config_password = os.environ["EMAIL_APP_PASSWORD"]
config_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
config_server_port = int(os.getenv("SMTP_PORT", "587"))
