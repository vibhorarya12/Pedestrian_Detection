a = 10
print(a)
def temp():
    global a
    a = 20

temp()
print(a)