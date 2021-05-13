FROM ubuntu:20.04

RUN apt update -y && \
    apt install -y python3-pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]
EXPOSE 5000
CMD [ "run.py" ]
