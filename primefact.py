import math as mn

class MyClass:
    def __init__(self, num):
        self.num = num
    
    def prime_fact(self):
        fact = []
        n = self.num
        while (n%2==0):
            fact.append(2)
            n = n // 2

        for i in range(3,int(mn.sqrt(n)),2):
            while (n%i==0):
                fact.append(i)
                n = n // i

        if(n>2):
            fact.append(n)
        print(fact)

def doTestPass(n):
    
    c = MyClass(n).prime_fact()
    print(c)
    
doTestPass(900)