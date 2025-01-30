# Constructor Telegram Bots
[**Constructor Telegram Bots**](https://constructor.exg1o.org/) is a website with which you can easily, free and without any programming knowledge, create your own multifunctional Telegram bot.

The website is non-commercial and does not aim to make money from its users.

The website was created because, unfortunately, all similar websites are commercial and aim to profit from their users, while the free plans on such sites severely restrict their users.

If you would like to support the project, you can make a [**donation**](https://constructor.exg1o.org/donation).<br>
Your donation will greatly help the development and improvement of the website.

## Requirements
- Linux
- Python 3.11.x
- PostgreSQL
- Redis

## Requirements from related projects.
- [Constructor Telegram Bots Frontend](https://github.com/EXG1O/Telegram-Bots-Hub#requirements)
- [Telegram Bots Hub](https://github.com/EXG1O/Telegram-Bots-Hub#requirements)

## Installing
1. To install, execute the following commands:
```bash
git clone --recurse-submodules https://github.com/EXG1O/Constructor-Telegram-Bots.git
cd Constructor-Telegram-Bots
source install.sh
```
2. Go to the `./frontend` directory to build the frontend and go back.
```bash
cd ./frontend
npm i
npm run build
cd ..
```
3. Now, go to the main page `http://127.0.0.1:8000` and log in.
4. Edit the `user` table in the database by changing the values of `is_staff` and `is_superuser` to `true` for the `Anonymous` user record.
5. Open the admin panel's main page `http://127.0.0.1:8000/admin` and select `Telegram Bots Hubs` -> `Hubs`.
6. Click `Add Hub`, enter all the necessary data, and copy the `Service Token`.
7. Deploy the [Telegram Bots Hub](https://github.com/EXG1O/Telegram-Bots-Hub) project and run it **(working in the global network)**.

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
