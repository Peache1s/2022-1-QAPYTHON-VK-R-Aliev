#!/bin/bash 
if [ $# -eq 2 ]
then
echo "N    URL:" >  $2
awk -F\" '{print $2}' $1 | awk '{print $2}' | sort | uniq -c | sort -r | head >> $2
else
echo "Введите 2 параметра! Первый параметр это файл acces.log, второй - файл для вывода! "
fi