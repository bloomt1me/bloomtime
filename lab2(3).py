import pandas as pd
import random

try:
    
    df = pd.read_csv(r"D:\USER\ONEDRIVE\桌面\Python\books-en.csv", 
                    encoding="cp1252",
                    on_bad_lines='skip', 
                    engine='python')       
    print("文件读取成功")
    
except Exception as e:
    print(f"读取文件时出错: {e}")
   
    try:
        df = pd.read_csv(r"D:\USER\ONEDRIVE\桌面\Python\books-en.csv", 
                        encoding="utf-8",
                        on_bad_lines='skip',
                        engine='python')
        print("使用UTF-8编码读取成功")
    except Exception as e:
        print(f"UTF-8编码也失败: {e}")
        exit()


print(f"数据形状: {df.shape}")
print(f"列名: {df.columns.tolist()}")


if len(df) < 20:
    print(f"警告: 数据只有 {len(df)} 行，将使用所有可用数据")
    random_records = df
else:
    random_records = df.sample(n=20)


try:
    with open("bibliography_en.txt", "w", encoding="utf-8") as f:  
        for i, (_, row) in enumerate(random_records.iterrows(), 1):
           
            author = row.get('Author', 'Unknown Author')
            title = row.get('Title', 'Unknown Title') 
            year = row.get('Year', 'Unknown Year')
            
            entry = f"{author}. «{title}» - {year}"
            f.write(f"{i}. {entry}\n")  
    
    print("书目引用已保存至 bibliography_en.txt")
    
except Exception as e:
    print(f"保存文件时出错: {e}")