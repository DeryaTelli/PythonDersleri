import time

def myFunc1():
    print("first function start:")
    time.sleep(5)
    print("first function end")
    return 5

def myFunc2():
    print("second function start:")
    time.sleep(5)
    print("second function end")
    return 10



#senkron islerin sirasiyla yapilmasi
#senkron kodlar
x=5
y=4
print(x+y)

if __name__=='__main__':
    myList=[10,20,30,40,50]
    print("loop start")
    for num in myList:
        print(num)
    print("loop end")

    a=myFunc1()
    b=myFunc2()
    print(f"my func first of result a's values {a}")
    print(f"my func second of result b's values {b}")