from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/socialmedia_frontend/navigation/profle.md')

def check_list(inp,lst):
    if inp in lst:
        return "New Input"
    else:
        return inp

class database:
    def __init__(self):
        self.id = 0
        self.userData = self.loadData()
        self.usernames = []
        self.passwords = []
        for dct in self.userData:
            self.usernames.append(dct["username"])
            self.passwords.append(dct["password"])
        print(self.usernames)
        print(self.passwords)
    def identify(self,index):
        self.id = index
    def createAccount(self,iname,ipass):
        if iname in self.usernames:
            print("Username already exist")
        else:
            self.id = self.userData[-1]["id"] + 1
            self.usernames.append(iname)
            self.passwords.append(ipass)
            self.userData.append({"id":self.id,"username":iname,"password":ipass})
            self.saveData(self.userData)
    def information(self,index):
        return self.userData
    def saveData(self,data):
        with open("Database.json", "w") as file:
            json.dump(data, file, indent=4)
    def loadData(self):
        with open("Database.json", "r") as file:
            data = json.load(file)
        return data
    def resetData(self):
        self.saveData([])
    def deleteAccount(self,index):
        self.userData.delete(index)

class User:
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = check_list(password,Database.passwords)
        self.uposts = []
    def login(self,iname,ipass):
        if iname in Database.usernames:
            if ipass in Database.passwords:
                if Database.usernames.index(iname) == Database.passwords.index(ipass):
                    i = Database.usernames.index(iname)
                    Database.identify(i)
                else:
                    print("Username or password is incorrect")
            else:
                print("Username or password is incorrect")
        else:
            print("Username or password is incorrect")
    def signout(self):
        self.name = ''
        self.password = ''
        self.id = ''
        self.email = ''
    def post(self,pdata):
        if self.id != '':
            pid = len(Database.posts)
            Database.posts.append(pdata)
            self.uposts.append(pid)

Database = database()
print(Database.userData)

print("Create new account?(y/n)")
ans = input()
if ans == "y":
    name = input("Please enter your name: ")
    password = input("Please enter you password: ")
    Database.createAccount(name,password)
elif ans == "n":
    print("Login")
    name = input("Please enter your name: ")
    password = input("Please enter you password: ")

user = User(Database.id,name,"fakemail123@gmail.com",password)
user.login(name,password)

@app.route('/Database', methods=['GET'])
def get_data():
    with open('Database.json') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

