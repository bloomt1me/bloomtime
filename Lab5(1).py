import re

def process_text_file(filename):
    """
    Extract from text file:
    1. Words containing hyphens
    2. Content inside parentheses
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:  # 打开文件，使用UTF-8编码
            text = file.read()  # 读取整个文件内容到字符串变量
    except FileNotFoundError:  # 如果文件不存在
        print(f"File {filename} not found.")  # 打印错误信息
        return  # 退出函数
    
    # 使用正则表达式查找所有包含连字符的单词
    hyphen_words = re.findall(r'\b\w+-\w+\b', text)
    
    # 查找所有括号内的内容（包括括号本身）
    parentheses_content_with_brackets = re.findall(r'\([^)]+\)', text)
    # 查找所有括号内的内容（不包括括号）
    parentheses_content = re.findall(r'\(([^)]+)\)', text)
    
    # 打印标题和分隔线
    print("=" * 50)
    print(f"Processing file: {filename}")  # 显示正在处理的文件名
    print("=" * 50)
    
    # 输出连字符单词部分
    print("\n1. Words containing hyphens:")  # 标题
    if hyphen_words:  # 如果有找到连字符单词
        for i, word in enumerate(hyphen_words, 1):  # 遍历列表，i从1开始
            print(f"{i}. {word}")  # 输出编号和单词
    else:  # 如果没有找到
        print("No hyphenated words found.")  # 输出提示信息
    
    # 输出括号内容（带括号）部分
    print("\n" + "-" * 50)  # 分隔线
    print("\n2. Content inside parentheses (with parentheses):")  # 标题
    if parentheses_content_with_brackets:  # 如果有找到括号内容
        for i, content in enumerate(parentheses_content_with_brackets, 1):  # 遍历列表
            print(f"{i}. {content}")  # 输出编号和内容
    else:  # 如果没有找到
        print("No parentheses content found.")  # 输出提示信息
    
    # 输出括号内容（不带括号）部分
    print("\n3. Content inside parentheses (without parentheses):")  # 标题
    if parentheses_content:  # 如果有找到括号内容
        for i, content in enumerate(parentheses_content, 1):  # 遍历列表
            print(f"{i}. {content}")  # 输出编号和内容
    else:  # 如果没有找到
        print("No parentheses content found.")  # 输出提示信息
    
    # 输出统计信息
    print("\n" + "=" * 50)  # 分隔线
    print("Statistics:")  # 标题
    print(f"Number of hyphenated words: {len(hyphen_words)}")  # 连字符单词数量
    print(f"Number of parentheses content: {len(parentheses_content_with_brackets)}")  # 括号内容数量

# 主程序入口
if __name__ == "__main__":  # 当直接运行此脚本时
    file_path = r"D:\USER\ONEDRIVE\桌面\Python\task1-ru.txt"  # 定义文件路径（原始字符串）
    process_text_file(file_path)  # 调用处理函数