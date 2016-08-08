while True:
    choice = raw_input("> ")
    execfile("test2.py")
    if choice == 'b' :
        print "You win"
        input("yay")
        break

raw_input()