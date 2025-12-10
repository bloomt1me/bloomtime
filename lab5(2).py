import re  # 导入正则表达式模块

def extract_com_links(html_content):  # 定义提取.com链接的函数
    """
    Extract all links to .com domains from HTML content.
    """
    # 匹配.com域名的URL模式
    # 这个模式可以捕获多种形式：href="...", src="...", url(...)等
    pattern = r'(?:href|src|url)\s*=\s*["\']([^"\']*\.com[^"\']*)["\']'
    # (?:href|src|url) - 非捕获组，匹配href、src或url
    # \s*=\s* - 匹配等号，两边可能有空格
    # ["\'] - 匹配单引号或双引号
    # ([^"\']*\.com[^"\']*) - 捕获组：匹配包含.com且不包含引号的字符串
    # ["\'] - 匹配结束引号
    
    # 查找所有匹配项
    com_links = re.findall(pattern, html_content, re.IGNORECASE)  # 忽略大小写匹配
    
    # 查找其他上下文中的URL
    pattern2 = r'https?://[^/\s]+\.com[^\s"\']*'
    # https?:// - 匹配http://或https://
    # [^/\s]+ - 匹配一个或多个非斜杠/非空白字符（域名部分）
    # \.com - 匹配.com
    # [^\s"\']* - 匹配零个或多个非空白、非引号字符（URL其余部分）
    additional_links = re.findall(pattern2, html_content, re.IGNORECASE)  # 忽略大小写匹配
    
    # 合并并去除重复项
    all_links = list(set(com_links + additional_links))  # 使用set去重，转回list
    
    return all_links  # 返回所有.com链接

def process_html_file(file_path):  # 定义处理HTML文件的函数
    """
    Process HTML file and extract .com domain links.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:  # 尝试UTF-8编码打开
            html_content = file.read()  # 读取整个文件内容
    except FileNotFoundError:  # 文件不存在异常
        print(f"File {file_path} not found.")  # 打印错误信息
        return []  # 返回空列表
    except UnicodeDecodeError:  # 编码错误异常
        try:
            with open(file_path, 'r', encoding='latin-1') as file:  # 尝试Latin-1编码
                html_content = file.read()  # 读取文件内容
        except Exception as e:  # 其他异常
            print(f"Error reading file: {e}")  # 打印错误信息
            return []  # 返回空列表
    
    # 提取.com链接
    com_links = extract_com_links(html_content)  # 调用提取函数
    
    # 显示结果
    print("=" * 70)  # 打印70个等号分隔线
    print(f"Processing HTML file: {file_path}")  # 显示正在处理的文件
    print(f"Found {len(com_links)} link(s) to .com domains")  # 显示找到的链接数量
    print("=" * 70)  # 打印分隔线
    
    if com_links:  # 如果有找到链接
        print("\nLinks to .com domains:")  # 打印标题
        for i, link in enumerate(sorted(com_links), 1):  # 遍历排序后的链接，从1开始编号
            print(f"{i:2}. {link}")  # 格式化输出：2位编号，后面跟链接
    else:  # 如果没有找到链接
        print("\nNo .com domain links found.")  # 打印提示信息
    
    # 附加分析
    print("\n" + "-" * 70)  # 打印分隔线
    print("Analysis by domain:")  # 打印分析标题
    
    # 按域名分组
    domain_groups = {}  # 创建空字典存储域名分组
    for link in com_links:  # 遍历所有链接
        # 从URL中提取域名
        domain_match = re.search(r'https?://(?:www\.)?([^/]+)', link, re.IGNORECASE)
        # https?:// - 匹配http://或https://
        # (?:www\.)? - 非捕获组，匹配可选的www.
        # ([^/]+) - 捕获组：匹配域名部分（直到第一个斜杠）
        if domain_match:  # 如果匹配成功
            domain = domain_match.group(1).lower()  # 获取域名并转为小写
            if domain in domain_groups:  # 如果域名已在字典中
                domain_groups[domain].append(link)  # 添加链接到现有列表
            else:  # 如果域名不在字典中
                domain_groups[domain] = [link]  # 创建新键值对
    
    if domain_groups:  # 如果有域名分组
        for domain, links in sorted(domain_groups.items()):  # 遍历排序后的域名
            print(f"\n  {domain}: {len(links)} link(s)")  # 打印域名和链接数量
            for link in links[:3]:  # 显示每个域名的前3个链接
                print(f"    - {link}")  # 打印链接
            if len(links) > 3:  # 如果链接超过3个
                print(f"    ... and {len(links) - 3} more")  # 显示剩余数量
    else:  # 如果没有域名分组
        print("  No domains found.")  # 打印提示信息
    
    return com_links  # 返回找到的链接列表

# 主程序执行
if __name__ == "__main__":  # 当直接运行此脚本时
    # 使用绝对路径
    html_file_path = r"D:\USER\ONEDRIVE\桌面\Python\task2.html"  # HTML文件路径（原始字符串）
    
    # 处理HTML文件
    com_links = process_html_file(html_file_path)  # 调用处理函数
    
    # 可选：将结果保存到文件
    if com_links:  # 如果找到了链接
        output_file = "com_links_results.txt"  # 输出文件名
        try:
            with open(output_file, 'w', encoding='utf-8') as f:  # 打开输出文件
                f.write("Links to .com domains found:\n")  # 写入标题
                f.write("=" * 50 + "\n")  # 写入分隔线
                for link in sorted(com_links):  # 遍历排序后的链接
                    f.write(f"- {link}\n")  # 写入链接
            print(f"\nResults saved to: {output_file}")  # 打印保存成功信息
        except Exception as e:  # 捕获异常
            print(f"Error saving results: {e}")  # 打印错误信息