#!/bin/bash
echo "Клонирование репозитория john с подмодулями..."
git clone --recurse-submodules https://github.com/openwall/john.git

echo "Установка зависимостей..."
sudo apt-get update
sudo apt-get install -y build-essential libssl-dev zlib1g-dev

echo "Установка hashcat..."
sudo apt install -y hashcat

echo "Установка redis-server..."
sudo apt install -y redis-server

echo "Установка celery..."
sudo apt install -y celery

echo "Установка websockets..."
sudo apt install python3-websockets

echo "Установка виртуального окружения..."
sudo apt-get update && sudo apt-get upgrade -y
sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate

pip install fastapi uvicorn celery redis aioredis requests
^C

cd john/src

echo "Запуск configure..."
./configure

echo "Компиляция проекта..."
make -s clean && make -sj4

cd ../..

echo "Запуск..."
uvicorn main:app --reload --port 8000

