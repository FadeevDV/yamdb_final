FROM python:3.8.5
WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
ADD entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
