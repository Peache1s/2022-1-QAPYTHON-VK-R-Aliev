Создано по 5 скриптов bash и python скриптов в соответствии с заданием:
BASH скрипты:
Все Bash скрипты написаны при помощи утилит linux, в частности awk:
При запуске каждого bash скрипта необходимо в качестве первого параметра передать название log файла, в качестве второго название файла для записи результатов:
Пример: 

./4xx_requests.sh /Users/peache1s/Downloads/access.log 4xx_requests.txt

Принцип всех bash скриптов одинаковый: выделение при помощи awk нужных полей, применение к ним регулярных выражений, сортировка и подсчет их с помощью утилит linux


Python скрипты: 
При запуске аналогично bash скриптам нужно указать два обязательных позиционных параметра, а также можно 
указать необязательный флаг --json "имя_файла", чтобы создавался файл json с итоговыми данными

Python скрипты также работают одинаково: при помощи цикла проходятся все строки и собираются в списки элемтов и их числам, которые после преобразуются в словарь/другой список, сортируются и получается результат
