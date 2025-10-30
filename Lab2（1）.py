import csv

count = 0
with open("D:\\USER\\ONEDRIVE\\桌面\\Python\\books-en.csv", encoding='cp1252') as file:
    reader = csv.DictReader(file, delimiter=";")
    for row in reader:
        if len(row["Book-Title"]) > 30:
            count += 1

print(count)   