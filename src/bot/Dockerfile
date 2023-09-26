FROM python:3.11-slim
RUN pip install "poetry==1.2.0"
COPY ./ .
WORKDIR /app
CMD ["gunicorn", "you_can_bot.wsgi:application", "--bind", "0:8000" ]
