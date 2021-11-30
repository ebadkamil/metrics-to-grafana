FROM python:3.8-slim-buster

RUN mkdir -p /home/code
COPY . /home/code
RUN pip install /home/code
CMD ["start_load_publisher"]