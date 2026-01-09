x=int(input("Enter value:"))
y=int(input("Enter value:"))
arithmatics=input("add/sub/mul/div")
if arithmatics=='add':
    print(x+y)
elif arithmatics=='sub':
    print(x-y)
elif arithmatics=='mul':
    print(x*y)
elif arithmatics=='div':
    print(x/y)
else:
    print("invalid input")
