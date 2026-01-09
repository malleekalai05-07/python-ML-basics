class Employee:
    def __init__ (self,name,salary):
        self.name=name
        self.salary=salary
    def display(self):
        print("Employee name:",self.name)
        print("Employee salary:",self.salary)
        
    def bonus(self):
        self.salary+=2000
        print("your bonus added")
class Tourist:
    def __init__(self,expense,place):
        self.expense=expense
        self.place=place
    
    def display(self):
        print("expense:",self.expense)
        print("tourist place:",self.place)
    def food(self,wallet):
        self.expense-=wallet
        print("due to expenses deduct amount from your wallet")
        print("your expenses is:",self.expense)
    def resort(self,wallet):
        self.expense-=wallet
        print("deducted amount from wallet")
        print("reamin:",wallet)
    
emp=Employee('A',3000)
emp.display()
emp.bonus()
emp.display()

tour=Tourist(6000,'ooty')
place=input("enter your place:")

if place=='ooty':
    print("Enjoy your journey")
else:
    print("choose best place to visit")
wallet=int(input("Enter your amount:"))
emp.wallet()


tour.display()



