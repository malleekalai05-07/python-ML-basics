num=int(input("Enter num:"))
if num%3==0 and num%5==0:
    print("The num is divisible by 3 and 5")
elif num%3!=0 and num%5==0:
    print("The num is no divisible by 3 and divisible by 5")
elif num%3==0 and num%5!=0:
    print ("The numbber is divisible by 3 and not divisible by 5")
else:
    print("The num is not divisible by 3 and 5")