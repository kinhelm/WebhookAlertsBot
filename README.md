# Webhook Alert Telegram Bot

This is a webhook to broadcasts alerts to all Telegram active chats.

## Requirements

- Python 3.8 or higher
- pip

## Installation

1. Clone the repository
2. Install the dependencies with pip:

```bash
pip install -r requirements.txt
```

## Usage

1- Run the Webhook with the following command:
```bash
python main.py
```
2- Run the Bot backend (to register Users) with the following command:
```bash
python bot.py
```
3- Send a POST request to the /push-alert endpoint with the tools you want.

Request body example:

```json
{
    "message": "My alert !"
}
```
