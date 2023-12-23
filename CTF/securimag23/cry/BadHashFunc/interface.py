from hash import hash
from colored import attr, fg, bg
from flag import flag
from sys import exit

passwd_hash = "7563667261747d00"
reset = attr(0)

print("Bienvenue sur mon interface securisée")
password = input("Veuillez rentrer le mot de passe de l'administrateur\n > ")

if passwd_hash != hash(password):
    print(bg(196) + "LEAVE!!!" + reset)
    exit(1)

print("Welcome admin! What do you want to do?")
while(True):
    print("1 - print flag")
    print("2 - exit")
    choice = int(input("Choice ?"))
    if choice == 1:
        print("Yes, the flag is " + fg(10)+ "{}".format(flag) + reset)
    elif choice == 2:
        break

print("Goodbye admin")
