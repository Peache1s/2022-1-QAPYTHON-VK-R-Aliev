#!/bin/bash
if [ $# -eq 2 ]
then  
echo "Число запросов: " > $2
awk -F\" '{print $2}' $1 | awk '{print $2}' | awk '/^\/|^http/{print $0}' | wc -l >> $2
else
echo "Введите 2 параметра! Первый параметр это файл acces.log, второй - файл для вывода! "
fi