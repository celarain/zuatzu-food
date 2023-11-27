FROM python:3.11.5

RUN pip install requests
RUN pip install beautifulsoup4

RUN mkdir /app
COPY inausti.py algorri.py utils.py __init__.py .env /app

WORKDIR /app

CMD ["sh", "-c", "python3 inausti.py && python3 algorri.py"]