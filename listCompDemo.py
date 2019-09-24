class Student:
    def __init__(self, name, id):
        self.name = name
        self.student_id = id
    def __str__(self):
        return f"Name {self.name}, ID: {self.student_id}"

def demo_list_comp():
    all_students = []
    user_reply = ""
    while user_reply.upper() != "DONE":
        user_reply = input("enter student name or done to stop: ")
        if user_reply.upper() == "DONE":
            break
        student_id = input("Now enter the student ID: ")
        stu = Student(user_reply, student_id)
        all_students.append(stu)
    all_students.sort(key = lambda stu1: stu1.name )
    for student in all_students:
        print(student)

    sample_list = [ 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']
    vowels = ['a', 'e', 'i', 'o', 'u']

    new_list = [letter.upper() for letter in sample_list if letter in vowels]
    print(new_list)

if __name__ == '__main__':
    demo_list_comp()