a = compile("def myFunc():\n\tglobal banned\n\tbanned=[]\nmyFunc()","<stdin>","cexe"[::-1])
print(str(a))