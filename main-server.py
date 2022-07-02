import socket 
from threading import Thread
import random

from cv2 import destroyAllWindows

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address  = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

clients = []
nicknames = []
print("Server is running")

questions = ['When do we celebrate independence day in India? a)15th August b) 1st April c) 30th Feb d) All of the above '
            ,'What should you do if a masked man offers you a chocolate if you go home with him? a) Dance b) Go with him c) Shoot him d) Refuse the offer and tell your mom(Alive)'
            ,'Who is the prime minister of India(sorry could not think of a better question :|)? a) Jshlatt b) Narendra Modi c) Mick Gordon d) Dj Blyatman'
            ]

answers = ['a', 'd', 'b']

def remove(connection):
    if connection in clients:
        clients.remove(connection)

def picker(conn):
    pick = random.randint(0,len(questions)-1)
    print(pick)
    pick_question = questions[pick]
    pick_answer = answers[pick]



    return pick, pick_question, pick_answer
    
def popper(question,answer):
    questions.pop(question)
    answer.pop(answer)


def clientThread(conn,nickname):
    score = 0
    conn.send("Welcome to JOKER.exe".encode("utf-8"))
    conn.send("______________________________\n\n".encode("utf-8"))
    conn.send("Answer the following questions and you will be rewarded\n".encode("utf-8"))
    conn.send("Wrong answers will result in crashing of program or \nother COMPLICATIONS\n\n".encode("utf-8"))
    pick, pick_question, pick_answer = picker(conn)
    conn.send(pick_question.encode('utf-8'))
    while True:
        try:
            message = conn.recv(2048).decode("utf-8")
            print(message)
            if message:
                if message == pick_answer:
                    score += 1
                    reply = "You have selected the right answer. Your score is {}".format(score)
                    conn.send(reply.encode("utf-8"))
                else:
                    conn.send(("WA").encode("utf-8"))
                popper(pick, pick_answer)
                pick, pick_question, pick_answer = picker(conn)

            else:
                remove(conn)
                
        except:
            continue


while True:
    conn,addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    clients.append(conn)
    nicknames.append(nickname)
    print(nickname + " has connected")
    new_thread = Thread(target= clientThread,args = (conn,nickname))
    new_thread.start()
