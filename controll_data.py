
class Info_User():
    def __init__(self,username = '',password = ''): 
        self.username = username
        self.password = password

    def __str__(self):
        return self.username + " " + self.password
    
    def info(self):
        return self.username + " " + self.password
    