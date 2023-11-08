# Arisa Takenaka Trombley
# 2375446
# trombley@chapman.edu
# CPSC-408-02
# Assignment 1

# This file contains all of the functions for this program to work
# When this file runs it will pull up a program that examines the student database

import csv
import sqlite3
import random

states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
advisors = ["Jon Humphreys", "Harry Potter", "Derek Prate", "Ben Fellows", "Jillie Bean"]

# Filling in empty advisors
# conn = sqlite3.connect('/Users/cutec/OneDrive/Documents/CPSC_Courses/CPSC_408/StudentDB.sqlite')  # establish connection to db
# mycursor = conn.cursor()  # the cursor allows python to execute SQL statements

# for i in range(1,101):
#     rand_index = random.randint(0,4)
#     advisor = advisors[rand_index]
#     mycursor.execute("UPDATE Student SET FacultyAdvisor = ? WHERE StudentID = ?", (advisor, i, ))
# conn.commit()
#
# for i in range(101,201):
#     mycursor.execute("DELETE FROM Student WHERE StudentID = ?", (i, ))
# conn.commit()
# conn.close()

# reads in the csv to create the Database
def read_csv():
    conn = sqlite3.connect('/Users/cutec/OneDrive/Documents/CPSC_Courses/CPSC_408/StudentDB.sqlite')  # establish connection to db
    mycursor = conn.cursor()  # the cursor allows python to execute SQL statements
    with open('/Users/cutec/OneDrive/Documents/CPSC_Courses/CPSC_408/students.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            mycursor.execute("INSERT INTO Student('FirstName','LastName','Address','City','State','ZipCode','MobilePhoneNumber','Major', 'GPA', 'isDeleted') VALUES (?,?,?,?,?,?,?,?,?,0)" , (row['FirstName'],row['LastName'],row['Address'],row['City'],row['State'],row['ZipCode'],row['MobilePhoneNumber'],row['Major'], row['GPA'],)) # always a dangling tuple

        conn.commit() # also closes it

    csv_file.close()

# asks for user input until valid GPA
def getValidGPA():
    while True:
        try:
            gpa = float(input("Enter GPA: "))
            if 0.0 <= gpa <= 4.8:
                return gpa
            else:
                print("GPA must be between 0.0 and 4.8.")
        except ValueError:
            print("Invalid input.")

# asks for user input until valid Zip Code
def getValidZip():
    while True:
        try:
            zip_code = int(input("Enter Zip Code: "))
            if len(str(zip_code)) == 5:
                return zip_code
            else:
                print("Zip Code must be 5 digits long")
        except ValueError:
            print("Invalid input.")

# asks for user input until valid string
def getValidName(type):
    while True:
        try:
            if type == 1:
                name = input("Enter First Name: ")
            elif type == 2:
                name = input("Enter Last Name: ")
            elif type == 3:
                name = input("Enter Major: ")
            elif type == 4:
                name = input("Enter City: ")

            for character in name:
                if character.isnumeric():
                    raise Exception("Input cannot have any numbers")
            return name

        except Exception as e:
            print(e)

# asks for user input until valid Phone Number
def getValidNumber():
    while True:
        try:
            mobile_phone = input("Enter Mobile Phone Number: ")
            if len(mobile_phone) < 10:
                raise Exception("Phone number is too short")
            for digit in mobile_phone:
                if digit.isalpha():
                    raise Exception("Input cannot have any letters")
            return mobile_phone
        except Exception as e:
            print(e)

# asks for user input until valid Advisor
def getValidAdvisor():
    while True:
        m_advisor = input("Enter Advisor (Jon Humphreys, Harry Potter, Derek Prate, Ben Fellows, Jillie Bean): ")
        for advisor in advisors:
            if m_advisor == advisor:
                return m_advisor
        print("Invalid Advisor")

# asks for user input until valid State
def getValidState():
    while True:
        m_state = input("Enter State: ")
        for state in states:
            if m_state == state:
                return m_state
        print("Invalid State")

# displays every Student in the database
def displayStudents():
    conn = sqlite3.connect('/Users/cutec/OneDrive/Documents/CPSC_Courses/CPSC_408/StudentDB.sqlite')  # establish connection to db
    mycursor = conn.cursor()  # the cursor allows python to execute SQL statements
    Students = mycursor.execute("SELECT * FROM Student")

    for Student in Students:
        print(Student)

    conn.close()

# Defines and adds new Student into database
def addNewStudent():
    conn = sqlite3.connect('/Users/cutec/OneDrive/Documents/CPSC_Courses/CPSC_408/StudentDB.sqlite')  # establish connection to db
    mycursor = conn.cursor()  # the cursor allows python to execute SQL statements
    print("Information for new student")
    first_name = getValidName(1)
    last_name = getValidName(2)
    gpa = getValidGPA()
    major = getValidName(3)
    advisor = getValidAdvisor()
    address = input("Enter Address: ")
    city = getValidName(4)
    state = getValidState()
    zip_code = getValidZip()
    mobile_phone = getValidNumber()
    mycursor.execute("INSERT INTO Student(FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted) VALUES (?,?,?,?,?,?,?,?,?,?,0)", (first_name, last_name, gpa, major, advisor, address, city, state, zip_code, mobile_phone,))
    conn.commit()
    print("Added New Student")

# Updates student Major, Faculty Advisor, or Mobile Phone Number
def updateStudent(student_id, type, field):
    conn = sqlite3.connect('/Users/cutec/OneDrive/Documents/CPSC_Courses/CPSC_408/StudentDB.sqlite')  # establish connection to db
    mycursor = conn.cursor()  # the cursor allows python to execute SQL statements
    if type == 1:
        mycursor.execute("UPDATE Student SET Major = ? WHERE StudentId = ?",(field, student_id,))
    elif type == 2:
        mycursor.execute("UPDATE Student SET FacultyAdvisor = ? WHERE StudentId = ?",(field, student_id,))
    elif type == 3:
        mycursor.execute("UPDATE Student SET MobilePhoneNumber = ? WHERE StudentId = ?",(field, student_id,))
    conn.commit()
    conn.close()

    print("Updated student with ID:  " + student_id)

# Soft deletes a student from the database
def deleteStudent(student_id):
    conn = sqlite3.connect('/Users/cutec/OneDrive/Documents/CPSC_Courses/CPSC_408/StudentDB.sqlite')  # establish connection to db
    mycursor = conn.cursor()  # the cursor allows python to execute SQL statements
    mycursor.execute("UPDATE Student SET isDeleted = 1 WHERE StudentId = ?", (student_id,))
    print("Successfully deleted student with Student ID: " + student_id)
    conn.commit()
    conn.close()

# finds all student within the search
def findStudent(type, search):
    conn = sqlite3.connect('/Users/cutec/OneDrive/Documents/CPSC_Courses/CPSC_408/StudentDB.sqlite')  # establish connection to db
    mycursor = conn.cursor()  # the cursor allows python to execute SQL statements
    print("Results: ")
    if type == 1:
        Students = mycursor.execute("SELECT * FROM Student WHERE Major = ?", (search,))
    elif type == 2:
        Students = mycursor.execute("SELECT * FROM Student WHERE GPA = ?", (search,))
    elif type == 3:
        Students = mycursor.execute("SELECT * FROM Student WHERE City = ?", (search,))
    elif type == 4:
        Students = mycursor.execute("SELECT * FROM Student WHERE State = ?", (search,))
    elif type == 5:
        Students = mycursor.execute("SELECT * FROM Student WHERE FacultyAdvisor = ?", (search,))

    for student in Students:
        print(student)

    conn.commit()
    conn.close()


# The program
while True:
    print("\nOptions")
    print("1. Display all students")
    print("2. Add New Student")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Search/Display Student")
    print("6: Exit")
    try:
        option = float(input("Select an option: "))

        if option == 1:
            displayStudents()
        elif option == 2:
            addNewStudent()
        elif option == 3:
            student_id = input("Student ID for student you wish to update: ")
            isNotValidInput = True
            while isNotValidInput:
                print("\nUpdate by: ")
                print("1. Major")
                print("2. Advisor")
                print("3. Mobile Phone")
                field = input("What do you wish to update? ")

                if field == str(1):
                    major = input("Input New Major: ")
                    updateStudent(student_id, 1, major)
                    isNotValidInput = False
                elif field == str(2):
                    print("Input New Advisor")
                    advisor = getValidAdvisor()
                    updateStudent(student_id, 2, advisor)
                    isNotValidInput = False
                elif field == str(3):
                    print("Input New Mobile Phone")
                    mobile_phone = getValidNumber()
                    updateStudent(student_id, 3, mobile_phone)
                    isNotValidInput = False
                else:
                    print("Invalid input")

        elif option == 4:
            student_id = input("StudentID of student you wish to delete: ")
            deleteStudent(student_id)
        elif option == 5:
            isNotValidInput = True
            while isNotValidInput:
                print("\nSearch by: ")
                print("1. Major")
                print("2. GPA")
                print("3. City")
                print("4. State")
                print("5. Advisor")
                field = input("Select a field of search: ")

                if field == str(1):
                    print("Input Major you want to search by ")
                    major = getValidName(3)
                    findStudent(1, major)
                    isNotValidInput = False
                elif field == str(2):
                    print("Input GPA you want to search by ")
                    gpa = getValidGPA()
                    findStudent(2, gpa)
                    isNotValidInput = False
                elif field == str(3):
                    print("Input City you want to search by ")
                    city = getValidName(4)
                    findStudent(3, city)
                    isNotValidInput = False
                elif field == str(4):
                    print("Input State you want to search by ")
                    state = getValidState()
                    findStudent(4, state)
                    isNotValidInput = False
                elif field == str(5):
                    print("Input Advisor you want to search by ")
                    advisor = getValidAdvisor()
                    findStudent(5, advisor)
                    isNotValidInput = False
                else:
                    print("Invalid input")

        elif option == 6:
            print("Goodbye!")
            quit()
        else:
            print("Invalid Input")

    except ValueError:
        print("Invalid Input")










