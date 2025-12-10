import re  # 导入正则表达式模块
import csv  # 导入CSV文件处理模块

def extract_and_save_table(file_path, output_path):  # 定义提取数据并保存为CSV的函数
    """ 
    Extract data, create table, save as CSV
    """ 
    # 读取文件
    try:
        with open(file_path, 'r', encoding='utf-8') as f:  # 尝试用UTF-8编码打开文件
            content = f.read()  # 读取整个文件内容
    except:  # 如果UTF-8编码失败
        try:
            with open(file_path, 'r', encoding='cp1251') as f:  # 尝试用cp1251编码（俄语常用）
                content = f.read()  # 读取文件内容
        except:  # 如果所有编码都失败
            print("Cannot read file")  # 打印错误信息
            return False  # 返回False表示失败
    
    # 打印文件内容样本用于调试
    print(f"File content sample (first 500 chars):")  # 打印提示
    print(content[:500])  # 显示文件前500个字符
    print("\n" + "="*50 + "\n")  # 打印分隔线
    
    # 提取每种数据类型
    # 1. IDs - 提取ID（1到5位数字）
    ids = re.findall(r'\b\d{1,5}\b', content)  # 查找所有1-5位数字
    ids = list(set(ids))  # 使用set去重，再转回list
    
    # 2. Surnames - 提取姓氏（俄语和英语）
    surnames = re.findall(r'\b[A-ZА-ЯЁ][a-zа-яё]{2,}\b', content)  # 查找以大写字母开头，至少3个字母的单词
    surnames = list(set(surnames))  # 去重
    
    # 3. Emails - 提取电子邮件地址
    emails = re.findall(r'\b\S+@\S+\.\S+\b', content)  # 查找@符号前后有非空白字符，后面有点的格式
    emails = list(set(emails))  # 去重
    
    # 4. Dates - 尝试多种日期格式
    dates = []  # 创建空列表存储日期
    # 模式1: dd.mm.yyyy（日.月.年）
    dates1 = re.findall(r'\b\d{1,2}\.\d{1,2}\.\d{2,4}\b', content)
    # 模式2: yyyy-mm-dd（年-月-日）
    dates2 = re.findall(r'\b\d{4}-\d{1,2}-\d{1,2}\b', content)
    # 模式3: dd/mm/yyyy（日/月/年）
    dates3 = re.findall(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b', content)
    # 模式4: 查找"Дата"或"Date"后面的日期
    dates4 = re.findall(r'(?:Дата|Date)[:\s]+(\d[^,\s]+)', content, re.IGNORECASE)
    
    dates = list(set(dates1 + dates2 + dates3 + dates4))  # 合并所有找到的日期并去重
    
    # 5. Categories - 尝试多种类别提取模式
    categories = []  # 创建空列表存储类别
    # 模式1: 大写单词（2-4个字符）
    cat1 = re.findall(r'\b[A-ZА-Я]{2,4}\b', content)
    # 模式2: "cat"或"category"或"категория"后面的单词
    cat2 = re.findall(r'(?:cat|category|категория)[:\s]+(\w+)', content, re.IGNORECASE)
    # 模式3: 常见类别名称
    cat3 = re.findall(r'\b(user|admin|guest|moderator|пользователь|админ|гость)\b', content, re.IGNORECASE)
    
    categories = list(set(cat1 + cat2 + cat3))  # 合并所有类别并去重
    
    # 调试：打印找到的内容
    print(f"ID found: {len(ids)} - Sample: {ids[:5] if ids else 'None'}")  # 显示ID数量和前5个样本
    print(f"Surnames found: {len(surnames)} - Sample: {surnames[:5] if surnames else 'None'}")  # 显示姓氏信息
    print(f"Emails found: {len(emails)} - Sample: {emails[:5] if emails else 'None'}")  # 显示邮箱信息
    print(f"Dates found: {len(dates)} - Sample: {dates[:5] if dates else 'None'}")  # 显示日期信息
    print(f"Categories found: {len(categories)} - Sample: {categories[:5] if categories else 'None'}")  # 显示类别信息
    
    # 如果仍然没有日期或类别，尝试提取任何可能是日期的数据
    if not dates:  # 如果没有找到日期
        print("\nTrying alternative date patterns...")  # 打印提示
        # 查找任何可能是日期的数字（4-8位数字）
        all_numbers = re.findall(r'\b\d{4,8}\b', content)  # 查找4-8位数字
        print(f"Possible date numbers: {all_numbers[:10]}")  # 显示前10个可能的日期数字
    
    # 获取非空列表的最小长度
    valid_lists = [lst for lst in [ids, surnames, emails, dates, categories] if len(lst) > 0]  # 过滤出非空列表
    
    if not valid_lists:  # 如果所有列表都为空
        print("No data found at all!")  # 打印错误信息
        return False  # 返回False
    
    # 使用可用数据的最小长度
    num_rows = min(len(lst) for lst in valid_lists)  # 计算所有非空列表的最小长度
    
    print(f"\nCreating table with {num_rows} rows...")  # 打印创建表格的信息
    
    # 即使某些字段缺失也创建CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:  # 打开CSV文件用于写入
        writer = csv.writer(csvfile)  # 创建CSV写入器
        writer.writerow(['ID', 'Surname', 'Email', 'Date', 'Category'])  # 写入表头
        
        for i in range(num_rows):  # 循环每一行
            row = [  # 创建行数据，如果索引超出列表长度则用'N/A'填充
                ids[i] if i < len(ids) else 'N/A',  # ID
                surnames[i] if i < len(surnames) else 'N/A',  # 姓氏
                emails[i] if i < len(emails) else 'N/A',  # 邮箱
                dates[i] if i < len(dates) else 'N/A',  # 日期
                categories[i] if i < len(categories) else 'N/A'  # 类别
            ]
            writer.writerow(row)  # 写入行数据
    
    print(f"✓ CSV file created: {output_path}")  # 打印成功信息
    print(f"✓ Rows written: {num_rows}")  # 显示写入的行数
    
    return True  # 返回True表示成功

# 运行脚本
if __name__ == "__main__":  # 如果直接运行此脚本
    input_file = r"D:\USER\ONEDRIVE\桌面\Python\task3.txt"  # 输入文件路径
    output_file = r"D:\USER\ONEDRIVE\桌面\Python\table.csv"  # 输出CSV文件路径
    
    print("Extracting data from file...")  # 打印开始提取的提示
    print("=" * 60)  # 打印分隔线
    
    success = extract_and_save_table(input_file, output_file)  # 调用函数提取数据并保存
    
    if success:  # 如果成功
        print("\n✓ SUCCESS: CSV file created successfully!")  # 打印成功信息
    else:  # 如果失败
        print("\n✗ FAILED: Could not create CSV file")  # 打印失败信息