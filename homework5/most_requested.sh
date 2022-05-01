#!/bin/bash
if [ $# -eq 2 ]
then
echo "N    URL:" >  $2
awk -F\" '{print $2}' $1 | awk '{split ($2,a,"[?%#;!&+=]"); print a[1]}' | sort | uniq -c | sort -r | head >> $2
else
echo "Введите 2 параметра! Первый параметр это файл acces.log, второй - файл для вывода! "
fi