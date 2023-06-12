f = open("credentials/credentials_aws.txt")
lines=f.readlines()
host1=lines[0][7:-1].strip()
database1=lines[1][11:].strip()
user1=lines[2][7:].strip()
password1=lines[3][11:].strip()
port1=lines[4][7:].strip()
url1=lines[5][6:].strip()
f.close()

class credentials_data:
    def __init__(self):
        self.host = host1
        self.database = database1
        self.user = user1
        self.password = password1
        self.port = port1
        self.url = url1

    def hoster (self):
        return self.host

    def databaser (self):
        return self.database

    def userer (self):
        return self.user

    def passworder (self):
        return self.password

    def porter (self):
        return self.port

    def urler (self):
        return self.url