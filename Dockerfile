FROM python:3.5.2
MAINTAINER Anubha Mandal "anubha.mandal@sjsu.edu"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
