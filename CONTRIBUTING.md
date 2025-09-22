# Contributing
Thank you for considering contributing!<br>
We appreciate your help in making this project better.

## Installing
Deploy the project by following the "[Installing](https://github.com/EXG1O/Constructor-Telegram-Bots#installing)" section.<br>
However, depending on your needs, you can skip certain steps:
- **Frontend Deployment**. If you're working only on the backend and don't need the UI, you can skip steps 2 – 4 (inclusive).
- **Microservice Deployment**. If you are going to work on the backend part that is not related to the microservice for Telegram bots, you can skip steps 5 – 8 (inclusive).

## Code Formatting and Linting
To maintain a consistent code style, we use **ruff** as code formatter and linter, and **mypy** for type checking.

### ruff
To format your code, run the following command:
```bash
ruff format .
```

To check your code for linting issues, run the following command:
```bash
ruff check .
```
This will list any issues that need to be addressed.

To auto-fix these issues, run the following command:
```bash
ruff check --fix .
```

### mypy
To ensure that your code passes type checking, run the following command:
```bash
mypy .
```

## Testing
We prioritize code quality and early bug detection through tests. To run the tests, use the following command:
```bash
python manage.py test
```
If your changes require new tests, please add them to ensure complete coverage.

## Logs
All log files can be found in the `./logs` directory.

## Translations
If you'd like to contribute by improving translations, you can find all locale files in the `./locale` directory.

## Pull Requests
When submitting a PR, please ensure that:
1. Your code follows the project's coding standards.
2. All tests pass successfully.
3. Your changes are well-documented.
