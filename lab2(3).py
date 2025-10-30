import pandas as pd
import random


try:
    df = pd.read_csv(r"D:\USER\ONEDRIVE\桌面\Python\books-en.csv",
                    sep=';',
                    encoding="cp1252",
                    on_bad_lines='skip')
    print("文件读取成功！")
except Exception as e:
    print(f"读取文件失败: {e}")
    exit()

print(f"数据有 {len(df)} 行, {len(df.columns)} 列")
print("列名:", df.columns.tolist())  


print("\n前2行数据:")
print(df.head(2))


随机书籍 = df.sample(n=min(20, len(df)))

with open("my_books.txt", "w", encoding="utf-8") as f:
    for i, row in 随机书籍.iterrows():
        作者 = row["Book-Author"]
        书名 = row["Book-Title"]
        年份 = row["Year-Of-Publication"]
        f.write(f"{作者}. {书名} - {年份}\n")

print("完成！书目已保存到 my_books.txt")
