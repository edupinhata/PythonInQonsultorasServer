#!/usr/bin/env python3

import http.server
import http.client
import datetime
import json
import Core
from login import login
from primes import primes

#classe que conterá as informações a serem passadas para o JSON
#class table():

p = primes(2, 500, 20)

class MyHandler(http.server.BaseHTTPRequestHandler):
    

    def do_POST(self):
        if self.path=='/login':
            print("Received something here!")
            n = int(self.headers['Content-Length'])
            text = str(self.rfile.read(n), 'utf-8')
            #dado = json.loads(text)
            print(text)
            #authenticating
            answer = text.split(':')
            a = login('user.txt')
            if(a.confirmUser(answer[1],answer[3])):
                dadoSend = 'accept'
                print(dadoSend)
                self.send_response(http.client.OK)
                self.send_header('Content-Type', 'text/plain')
                self.send_header('Content-Type', len(dadoSend))
                self.end_headers()
                self.wfile.write(bytes(dadoSend,'utf-8'))
            else:
                dadoSend = 'reject';
                print(dadoSend)
                self.send_response(http.client.OK)
                self.send_header('Content-Type', 'text/plain')
                self.send_header('Content-Type', len(dadoSend))
                self.end_headers()
                self.wfile.write(bytes(dadoSend,'utf-8'))

        if self.path=='/update':
            print("Updating")
            n = int(self.headers['Content-Length'])
            text = str(self.rfile.read(n), 'utf-8')
            print(text)
            textList = text.split(';')
            p.update(textList[0], textList[1:])
            dadoSend = 'You are connected'
            self.send_response(http.client.OK)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Type', len(dadoSend))
            self.end_headers()
            self.wfile.write(bytes(dadoSend,'utf-8'))
        


        if self.path=='/add':
            print("Received something here!")
            n = int(self.headers['Content-Length'])
            text = str(self.rfile.read(n), 'utf-8')
            #dado = json.loads(text)
            print(text)
            #authenticating
            answer = text.split(':')
            a = login('user.txt')
            a.getPath()
            if(not(a.confirmUser(answer[1],answer[3]))):
                a.addUser(answer[1],answer[3])
                print('User added')
                dadoSend = 'added'
                print(dadoSend)
                self.send_response(http.client.OK)
                self.send_header('Content-Type', 'text/plain')
                self.send_header('Content-Type', len(dadoSend))
                self.end_headers()
                self.wfile.write(bytes(dadoSend,'utf-8'))


    def do_GET(self):
        if self.path == '/':
            f = open('index.html')
            string = f.read()
            # self.send_error(http.client.NOT_FOUND)
            self.send_response(http.client.OK)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(string))
            self.end_headers()
            self.wfile.write(bytes(string, 'utf-8'))
   
        elif self.path == '/instance':
            if(not(p.isFinished())):
                string = str('process:' + p.getProcessUnit())
                self.send_response(http.client.OK)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Type', len(string))
                self.end_headers()
                self.wfile.write(bytes(string, 'utf-8'))
            else:
                print(p.answer)

    

server = http.server.HTTPServer(('', 7777), MyHandler)
server.serve_forever()
