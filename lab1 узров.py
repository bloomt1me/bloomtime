left_half = [
    "  ******* ",
    "        * ",
    "        * ",
    "  ******* ",
    "    *     ",
    "    *     ",
    "  ******* "
]

for line in left_half:
    right_half = line[::-1]
    symmetric_line = line + right_half
    print(symmetric_line)