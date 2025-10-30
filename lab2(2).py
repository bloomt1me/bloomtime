import pandas as pd

df = pd.read_csv(r"D:\USER\ONEDRIVE\桌面\Python\books-en.csv", 
                sep=';', 
                encoding="cp1252")

print("Названия столбцов:", list(df.columns))

author = input("Введите имя автора: ")

price = df['Price'].astype(str).replace(',', '.')
print(price)
books = df[(df['Book-Author'] == author) & (price.astype(float) <= 200)]

print(f"Найдено {len(books)} книг:")
for i, row in books.iterrows():
    print(f"- {row['Book-Title']} (${row['Price']})")