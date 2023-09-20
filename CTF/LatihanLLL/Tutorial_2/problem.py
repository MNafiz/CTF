import random

coefs = [random.randrange(2**32) for _ in range(3)]
public = [random.randrange(2**128) for _ in range(3)]

S = sum([i*j for i,j in zip(coefs,public)])

print(f"{S = }")
print(f"{public = }")

with open("answer.txt","w") as f:
    f.write(str(coefs))
    f.close()