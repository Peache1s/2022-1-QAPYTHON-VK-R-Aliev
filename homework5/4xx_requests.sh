#!/bin/bash 
if [ $# -eq 2 ]
then
echo "SIZE:IP:           CODE: URL:" >  $2
awk '($9 ~ /4../)' $1 |awk '{split ($7,a,"[?%#;!&+=]"); print $10, $1, $9, a[1]}' | sort -rn | head -n 5 >> $2
else
echo "Введите 2 параметра! Первый параметр это файл acces.log, второй - файл для вывода!"
fi