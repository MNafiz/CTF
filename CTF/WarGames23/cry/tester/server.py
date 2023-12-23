msg = input("> ")
print(msg.encode(errors="surrogateescape").hex())