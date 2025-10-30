import math

x_values = range(0, 15)
height = 9

for y in range(height, 0, -1):
    row = ""
    for x in x_values:
        func_value = math.sqrt(x)
        if abs(y - 1 - func_value) < 0.6:
            row += "*"
        else:
            row += " "
    print(row)