class ATM:
  def  __init__(self,balance,pin):
    self.balance=balance
    self.pin=pin
  def check_balance(self):
    print("your balnce is:",self.balance)
  def Deposit(self,amount):
    self.balance+=amount
    print("deposited successfully")
    print("Updated balance",self.balance)
    print("--Thank you--")
  def withdraw(self,amount):
    if self.balance>=amount:
      self.balance-=amount
      print("withdraw successfully")
    else:
      print("insufficient balance")
    print("Thank you")
  def pin_change(self):
     if choose=='yes':
          self.pin!=new_pin
          print("pin is changed")
     else:
          print("sorry! we can not change your pin")
     print("Thank you")
  def transfer(self,amount):
    if self.balance>=amount:
     self.balance-=amount
     print("Transfer succefully") 
    else:
     print("Insufficient")
    print("Updated balance:",self.balance)
    print("Thank you")
  def exit(self):
    print("Thank you")

atm=ATM(9000,7865)
print("---/WELCOME/---")
pin=int(input("Enter your pin: "))
while True:
  if pin==atm.pin:
      print("\n---ATM OPEARTION---")
      print("a.check_balance")
      print("b.Deposit")
      print("c.withdraw")
      print("d.pin_change")
      print("e.transfer")
      print("f.exit")
  
      option=input("choose your option:")

      if option=='check_balance':
        atm.check_balance() 
      elif option=='Deposit':
          amount=float(input("enter your amount: "))
          atm.Deposit(amount)
      elif option=='withdraw': 
         amount=float(input("Enter your amount: "))
         atm.withdraw(amount)
      elif option=='pin_change':
         new_pin=int(input("enter your new pin: "))
         choose=input("yes or no:")
         atm.pin_change()
      elif option=='transfer':
         acc=int(input("Enter your acc no: "))
         ifsc=input("Enter your IFSC code: ")
         bank=input("you bank name ? ")
         amount=float(input("Enter your amount: "))
         atm.transfer(amount)
      elif option=='exit':
           atm.exit()
           break
      else:
          print("Invalid input")
  elif pin!=atm.pin:
     print("incorrect pin")
     break
  else:
   print("try agin later")
   

  
