# key = raw_input();
# 
# while bool(key):
# 	execfile("bmp180.py")
# 
# 	if bool(key) != True:
# 		break
import sys, select, os

i = 0
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    execfile("bmp180.py")
    print i
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = raw_input()
        break
    i += 1