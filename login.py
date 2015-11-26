#!/usr/bin//env python3

# class that will deal with the user control
import os
import re

class login:
    def __init__(self, path):
        self.FILE_PATH = path
        
    def confirmUser(self, user, pswd):
        if(os.path.exists(self.FILE_PATH)):
            with open(self.FILE_PATH) as f:
                lines = f.readlines()
        
            for line in lines:
                print('Line: ' + line.replace('\n',''))
                if(line.replace('\n','')==str(user+':'+pswd)):
                    print('I find it!')
                    return True
        return False

    def addUser(self, user,pswd):
        f = open(self.FILE_PATH, "a")
        f.write(str(user+':'+pswd+'\n'))

    def getPath(self):
        print(self.FILE_PATH)


        



