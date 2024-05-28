with open('names.txt',encoding="utf-8") as file:
    conntent:str = file.read()
names:list[str] = conntent.split()
for name in names:
    print(name)