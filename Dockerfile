FROM python:2.7

RUN mkdir /app
WORKDIR /app
ADD server/main.py /app

EXPOSE 5000
CMD ["python", "/app/main.py", "0.0.0.0", "5000"]
