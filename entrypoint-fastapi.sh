#!/bin/sh

while ! nc -z crypto_data-kafka-1  9092
do
    echo ">>>>>>>>>> Waiting for kafka... <<<<<<<<<<"
    sleep 2
done

uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
