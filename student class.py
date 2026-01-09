class Student:
    def __init__(self,name,roll_no,mark):
        self.name=name
        self.roll_no=roll_no
        self.mark=mark
        
    def student_name(self):
        print("Enter your name:",self.name)
    def student_roll_no(self):
        print("enter your roll_no:",self.roll_no)
    def mark(self):
        print("Enter mark ofstudent",self.mark)
    def dispaly(self):
        print("name",self.name)
        print("roll_no",self.roll_no)
        print("mark:",sum(self.mark))

name=(input("Enter your name:"))
roll_no=int(input("Roll_no:"))
mark=[]
mark.append(60)
mark.append(70)
mark.append(90)
mark.append(80)

std=Student(mark,name,roll_no)
std.display()
















