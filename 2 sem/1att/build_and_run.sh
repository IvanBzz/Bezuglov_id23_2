#!/bin/bash
echo "Клонирование репозитория john с подмодулями..."
git clone --recurse-submodules https://github.com/openwall/john.git

echo "Установка зависимостей..."
sudo apt-get update
sudo apt-get install -y build-essential libssl-dev zlib1g-dev

echo "Установка hashcat..."
sudo apt install -y hashcat

cd john/src

echo "Запуск configure..."
./configure

echo "Компиляция проекта..."
make -s clean && make -sj4

cd ../..

echo "Запуск main.py..."
python3 main.py
