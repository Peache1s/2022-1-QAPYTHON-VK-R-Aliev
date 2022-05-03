#!/bin/bash 
if [ $# -eq 2 ]
then
echo "N:     TYPE:" >  $2
awk -F\" '{print $2}' $1 | awk '{print $1}'|awk '/^[A-Z]/{print $0}' |sort | uniq -c | sort -rn >> $2
else
echo "Введите 2 параметра! Первый параметр это файл acces.log, второй - файл для вывода! "
fi