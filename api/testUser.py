import json

def check_list(inp,lst):
    if inp in lst:
        return "New Input"
    else:
        return inp

class database:
    def __init__(self):
        self.id = 0
        self.usernames = []
        self.passwords = []
        self.userData = self.loadData()
    def identify(self,index):
        self.id = index
    def createAccount(self,iname,ipass):
        if iname in self.usernames:
            pass
        else:
            self.id = len(self.usernames)
            self.usernames.append(iname)
            self.passwords.append(ipass)
            self.userData.append({"id":self.id,"name":iname,"password":ipass})
    def information(self,index):
        return {"id":index,"name":self.usernames[index],"password":self.passwords[index]}
    def saveData(self,data):
        with open("Database.json", "w") as file:
            json.dump(data, file, indent=4)
    def loadData(self):
        with open("Database.json", "r") as file:
            data = json.load(file)
        return data
    def resetData(self):
        self.saveData([])

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
                    Database.identify[i]
                    Database.saveData(Database.information(Database.id))
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


    
    