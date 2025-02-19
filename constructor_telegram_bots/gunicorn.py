from constructor_telegram_bots.settings import LOGS_DIR

workers = 9
max_requests = 1000
max_requests_jitter = 100

capture_output = True
accesslog = str(LOGS_DIR / 'gunicorn_info.log')
errorlog = str(LOGS_DIR / 'gunicorn_info.log')
