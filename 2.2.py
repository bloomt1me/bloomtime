# extra2_top20_popular.py
import pandas as pd

df = pd.read_csv(r"D:\USER\ONEDRIVE\桌面\Python\books-en.csv", 
                sep=';', 
                encoding="cp1252")

top20 = df.sort_values(by="Downloads", ascending=False).head(20)
print("最受欢迎的20本书:\n", top20[["Book-Title", "Book-Author", "Downloads"]])