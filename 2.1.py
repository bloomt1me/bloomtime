# extra1_unique_publishers.py
import pandas as pd

# Метод 1: Использование точки с запятой в качестве разделителя
df = pd.read_csv(r"D:\USER\ONEDRIVE\桌面\Python\books-en.csv", 
                sep=';', 
                encoding="cp1252")

unique_pubs = df["Publisher"].unique()
print("Количество уникальных издательств:", len(unique_pubs))
print("Список уникальных издательств: \n", unique_pubs)