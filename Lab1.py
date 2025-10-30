import time

WHITE = "\033[48;5;255m"  
RED = "\033[48;5;1m"      
RESET = "\033[0m"         

flag_height = 12  
flag_width = 40   

for _ in range(flag_height // 2):
    print(f"{WHITE}{' ' * flag_width}{RESET}")
    time.sleep(0.1)

for _ in range(flag_height // 2):
    print(f"{RED}{' ' * flag_width}{RESET}")
    time.sleep(0.1)