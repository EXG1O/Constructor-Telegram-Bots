# Constructor Telegram Bots
[**Constructor Telegram Bots**](https://constructor.exg1o.org/) is a website with which you can easily, free and without any programming knowledge, create your own multifunctional Telegram bot.

The website is non-commercial and does not aim to make money from its users.

The website was created because, unfortunately, all similar websites are commercial and aim to profit from their users, while the free plans on such sites severely restrict their users.

If you would like to support the project, you can make a [**donation**](https://constructor.exg1o.org/donation).<br>
Your donation will greatly help the development and improvement of the website.

## Requirements
- Linux
- Python 3.11
- PostgreSQL
- Redis

## Requirements from related projects.
- [Constructor Telegram Bots Frontend](https://github.com/EXG1O/Telegram-Bots-Hub#requirements)
- [Telegram Bots Hub](https://github.com/EXG1O/Telegram-Bots-Hub#requirements)

## Installing
1. First, installing the backend using the following commands:
```bash
git clone https://github.com/EXG1O/Constructor-Telegram-Bots.git
cd Constructor-Telegram-Bots
git checkout tags/v2.1.0
python -m venv env
source env/bin/activate
source install.sh
```
2. Now, we need to run the command to get tokens for a microservice:
```bash
python manage.py create_hub
```
3. Deploy the [Telegram Bots Hub](https://github.com/EXG1O/Telegram-Bots-Hub) project and run it **(working in the global network)**.
4. Finally, build the [frontend](https://github.com/EXG1O/Constructor-Telegram-Bots-Frontend#installing).

## Usage
1. To start we need two terminals and the following commands for each:
```bash
python manage.py runserver
```
```bash
celery -A constructor_telegram_bots worker --loglevel=INFO -f logs/celery.log
```
2. Open the home page `http://127.0.0.1:8000` and enjoy :)

## Contributing
Read [CONTRIBUTING.md](CONTRIBUTING.md) for more information on this.

## License
This repository is licensed under the [AGPL-3.0 License](LICENSE).
