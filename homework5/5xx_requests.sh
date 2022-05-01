#!/bin/bash
if [ $# -eq 2 ]
then
echo "N:   IP:" >  $2
awk '($9 ~ /5../)' $1 | awk '{print $1}'  | uniq -c | sort -rn | head -n 5 >> $2
else
echo "Введите 2 параметра! Первый параметр это файл acces.log, второй - файл для вывода!"
fi