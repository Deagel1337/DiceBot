# DiceBot

Dicebot for pen and paper

**This works only with Python 3**

<br>

## Launch locally

Steps to launch this bot

```
python -m pip install requirements.txt

Create a .env file with BOT_TOKEN="YOUR_TOKEN"

```
---
## With docker

**To build the image**
```
docker build -t paul_bot .
```

**To run the image**
```
docker run -d --name paul paul_bot
```