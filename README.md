# Constructor Telegram Bots

[Constructor Telegram Bots](https://constructor.exg1o.org/) is a user-friendly platform that lets you easily create your own multifunctional Telegram bot for free with no coding required.

## Motivation

The motivation for this project stemmed from observing that similar platforms are heavily commercialized with multiple subscription tiers. These tiers are quite expensive and don't actually eliminate limitations entirely, they simply make them less restrictive. Meanwhile, the free versions are usually not very useful.

[Constructor Telegram Bots](https://constructor.exg1o.org/) exists as a genuinely free alternative that doesn't compromise on functionality, allowing anyone to build powerful bots without artificial limitations.

## Quick Start

You can start using the platform immediately by visiting [**constructor.exg1o.org**](https://constructor.exg1o.org/).

Alternatively, you can self-host the platform using the installation instructions below.

## Requirements

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Security Recommendations

It is recommended to run Docker in [Rootless mode](https://docs.docker.com/engine/security/rootless/) for enhanced security. This prevents the Docker daemon from running with root privileges.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/EXG1O/Constructor-Telegram-Bots.git
cd Constructor-Telegram-Bots
git checkout tags/v1.0
git submodule update --init --recursive
```

### 2. Configure environment variables

Copy the example environment file and configure it with your settings:

```bash
cp .env.example .env
```

### 3. Create required directories

Create the following directories:

```bash
mkdir -p logs sockets static media
```

### 4. Start the platform

Run the Docker Compose services in the background:

```bash
docker compose up --build -d
```

To include the [Nginx](https://nginx.org/) reverse proxy, use:

```bash
docker compose --profile nginx up --build -d
```

If using [Nginx](https://nginx.org/), the platform will be accessible at `http://localhost:8000` (or your configured `HTTP_PORT`).

## Usage

Once the services are running, open your browser and navigate to the platform at `http://localhost:8000` to start creating your Telegram bots.

### Project directories

The following directories are created in the project root during initialization:

- `logs` - Contains logs from the [backend](https://github.com/EXG1O/Constructor-Telegram-Bots-Backend) and microservices ([Telegram Bots Hub](https://github.com/EXG1O/Telegram-Bots-Hub))
- `sockets` - Contains [Unix sockets](https://en.wikipedia.org/wiki/Unix_domain_socket) from the [backend](https://github.com/EXG1O/Constructor-Telegram-Bots-Backend) and microservices ([Telegram Bots Hub](https://github.com/EXG1O/Telegram-Bots-Hub))
- `static` - Contains static files served by the platform
- `media` - Contains user-uploaded media files

## License

This repository is licensed under the [AGPL-3.0 License](LICENSE).
