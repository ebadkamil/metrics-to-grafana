FROM python:3.8-slim-buster
WORKDIR /code
ADD . .
RUN pip install -e .
CMD ["start_load_publisher"]