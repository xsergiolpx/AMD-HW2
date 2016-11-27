import threading
from threading import Thread

def func1():
    print("fun1")
    print("fun1")
    print("fun1")
    print("fun1")
    print("fun1")

def func2():
    print("fun2")

if __name__ == '__main__':
    Thread(target = func1).start()
    Thread(target = func2).start()