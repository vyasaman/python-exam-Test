import pymysql
db = pymysql.connect(host='localhost', port=3306, user='root',
                     password='Aman@123', database='Exam')
cur = db.cursor()


class AddingClass:

    def addMember(self):
        uname = input("Enter Username of Member:- ")
        paswd = input('Create a Password for the User:- ')
        role = input('Enter Role of User(Student/Admin):- ')
        if role.lower() == 'student':
            cur.execute("insert into userdata(uname,pass,role) values('{}','{}','{}')".format(
                uname, paswd, role))
            db.commit()
            print('\nStudent Registered Successfully.\n')
        elif role.lower() == 'admin':
            cur.execute("insert into userdata(uname,pass,role) values('{}','{}','{}')".format(
                uname, paswd, role))
            db.commit()
            print('\nAdmin Added Succsessfully.\n')
        else:
            print('Invalid Role of User.')

    def addTechnology(self):
        while True:
            try:
                tname = input('Enter Technology Name;- ')
                cur.execute(
                    "insert into technology(t_name) values('{}')".format(tname))
                db.commit()
            except(Exception):
                print('\n\nTechnology Already Exist.')
            finally:
                i = input('\n\nDo You want to add Another Technology (Y/N):-  ')
                if i.lower() == 'y':
                    continue
                elif i.lower() == 'n':
                    break

    def addQuestion(self):
        try:
            ques = input('\n\n\n\nEnter The Question :- \n')
            op1 = input('Enter Option a:-')
            op2 = input('Enter Option b:-')
            op3 = input('Enter Option c:-')
            op4 = input('Enter Option d:-')
            corAns = input('Enter Correct Option (a/b/c/d):- ')
            cur.execute('select * from technology order by tid asc')
            res = cur.fetchall()
            print('Select Tech Id from the List:- ')
            for i in res:
                print(i[0], '\t', i[1])
            techid = int(input('Enter Tech Id From the above List;- '))

            cur.execute(
                "insert into question(question,op1,op2,op3,op4,correct,techID) values('{}','{}','{}','{}','{}','{}',{})".format(ques, op1, op2, op3, op4, corAns, techid))
            db.commit()
            print('\n\n\n')
        except(Exception):
            print('\n\nQuestion Already Exist. Please Enter Another Question.\n\n')


class Test:
    tech = None

    def startTest(self, uid):
        cur.execute('select * from technology')
        res = cur.fetchall()
        self.tech = res
        print('Select Tech Id from the List:- ')
        for i in res:
            print(i[0], '\t', i[1])
        id = int(input("Enter Tech Id Whose Exam You want to give:- "))
        cur.execute("Select * from question where techID={}".format(id))
        res1 = cur.fetchall()
        a = 1
        score = 0
        for x in res1:
            print('Q'+str(a), '.', x[1], '\na.', x[2],
                  '\tb.', x[3], '\nc.', x[4], '\td.', x[5], '\n')
            ans = input('Enter Correct Option (a/b/c/d)"- ')
            if ans.lower() == x[6].lower():
                score += 1
            a += 1
        marks = (score/len(res1))*100
        status = ''
        if marks >= 40:
            status = 'Pass'
        else:
            status = 'Fail'
        cur.execute(
            "insert into results(uid,techID,marks,resDate,status) values({},{},{},NOW(),'{}')".format(uid, id, marks, status))
        db.commit()

    def Results(self, uid, uname):
        cur.execute("Select * from results where uid={}".format(uid))
        res = cur.fetchone()
        print('\n\n----------\tResults \t ----------\n\n')
        print("\nId \t\t\t\t", uid, '\n\nName \t\t\t\t', uname, '\n\nExam Submission Date and Time   ',
              res[4], '\n\nTechnology   \t\t\t', self.tech, '\n\nMarks Obtained     \t\t '+str(res[3])+'%\n\nStatus \t\t\t\t', res[5])
        input('\n\nPress Enter to exit Results tab.:- \n')


class Login(AddingClass, Test):

    def student(self, res):
        print('---------- \t Welcome', res[1], '\t ----------')
        while True:
            sch = int(
                input('\n\nEnter Your Choice\n\n1. Start Test\n2. Results\n3. Logout.\n'))
            if sch == 1:
                print('\n\n')
                self.startTest(res[0])
            elif sch == 2:
                print('\n\n')
                self.Results(res[0], res[1])
            elif sch == 3:
                print('\n\n')
                break

    def admin(self, res):
        print('Welcome', res[1], '\n')
        while True:
            ach = int(input(
                'Enter Your Choice\n\n1. Add Student\n2. Add Technology\n3. Add Question\n4. Logout.'))
            if ach == 1:
                print('\n\n')
                self.addMember()
            elif ach == 2:
                print('\n\n')
                self.addTechnology()
            elif ach == 3:
                print('\n\n')
                self.addQuestion()
            elif ach == 4:
                print('\n\n')
                break
            else:
                print('\n\n')
                print('Invalid Input.')


obj = Login()

print('-------------Welcome.------------\n\n\tPlease Login\n')
while True:
    u_id = int(input('Enter Username/Id:- '))
    pswd = input('Enter Password:- ')
    cur.execute(
        "Select * from userdata where uid={} and pass='{}'".format(u_id, pswd))
    res = cur.fetchone()
    if u_id in res and pswd in res:
        if res[3].lower() == 'admin':
            print('\n\n')
            obj.admin(res)
        elif res[3].lower() == 'student':
            print('\n\n')
            obj.student(res)
    else:
        print('Incorrct ID or Password.')

    inp = input('Do you Want to Exit(Y/N):-').lower()
    if inp == 'y':
        break
