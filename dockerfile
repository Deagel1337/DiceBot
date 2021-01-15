FROM python:3.8.5

WORKDIR /DiceBot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python","./paul_bot.py"]