data = {"positive": 0, "negative": 0, "zero": 0}
with open(r"D:\USER\ONEDRIVE\桌面\Python\sequence.txt", 'r', encoding='utf-8') as file:
    for line in file:
        number = float(line.strip())
        if number > 0:
            data["positive"] += 1
        elif number < 0:
            data["negative"] += 1
        else:
            data["zero"] += 1

total_sum = sum(data.values())
percentages = {category: (value / total_sum) * 100 for category, value in data.items()}

chart_height = 10

for i in range(chart_height, 0, -1):
    row = ""
    for category in ["positive", "negative", "zero"]:  
        percentage = percentages[category]
        if (percentage / 100) * chart_height >= i:
            row += "█ "  
        else:
            row += "  "  
    print(row)

labels_row = "positive negative zero "
percentages_row = f"{percentages['positive']:.1f}% {percentages['negative']:.1f}% {percentages['zero']:.1f}% "  # 修正：f-string语法
print(labels_row)
print(percentages_row)