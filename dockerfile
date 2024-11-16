FROM python:slim-bullseye

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend /app/

EXPOSE 5000

CMD ["python", "run.py"]
