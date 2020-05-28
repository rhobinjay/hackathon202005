from alpine:latest

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

WORKDIR /scheduler_app

COPY . /scheduler_app

RUN pip3 --no-cache-dir install -Ir requirements.txt

EXPOSE 5001

ENTRYPOINT ["python3"]
CMD ["app.py"]
