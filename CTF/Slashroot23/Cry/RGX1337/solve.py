import re

with open("flags.txt", "r") as f:
    content = f.read()
    f.close()

# content = content.split("\n")

pattern = "slashroot7\{[A-Z]+[0-9]+[a-z]+[A-Z]+\}"
possible = re.findall(pattern, content)
print(possible)