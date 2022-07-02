import socket
from tkinter import *
from threading import Thread
import pyttsx3


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = "127.0.0.1"
port = 8000

client.connect((ip_address,port))

class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.withdraw()

        self.loginWin = Toplevel()
        self.loginWin.title = "LoGiN0"
        self.loginWin.resizable(width = False, height = False)

        self.loginWin.configure(width= 400, height = 300)

        self.pls = Label(self.loginWin,
        text = "Enter y0ur n@ame",
        justify = CENTER,
        font ="Zalgo 14 bold" )

        self.pls.place(
        relheight=0.14,
        relx = 0.2,
        rely = 0.07)

        self.labelName = Label(self.loginWin,
        text = "Name: ",
        font = "Helvetica 12")

        self.labelName.place(
        relheight = 0.2,
        relx = 0.1,
        rely = 0.2)
        
        self.entryName = Entry(self.loginWin,font = "Helvetica 12")
        self.entryName.place(
        relwidth = 0.4,
        relheight = 0.09,
        relx = 0.35,
        rely = 0.26)

        self.entryName.focus()

        self.go = Button(
            self.loginWin, 
            text = "Continue",
            font = "Helvetica 12 bold",
            command=lambda:self.proceed(self.entryName.get())
            )
        self.go.place(
            relx = 0.4,
            rely = 0.44)
        
        self.window.mainloop()

    def proceed(self,name):
        self.loginWin.destroy()
        self.layout(name) 
        rcv = Thread(target = self.receive)
        rcv.start()

    def layout(self,name):
        self.name = name
        self.window.deiconify()
        self.window.title("Main window")
        self.window.resizable(width = False, height = False)
        self.window.configure(width = 470, height = 550,bg = "#000000")

        self.labelHead = Label(self.window,text = "Successfully initiallized new client",bg = "#000000", fg = "green", font = "CORNERSTONE  18", pady = 5)
        self.labelHead.place(relheight= 0.5)

        self.textcons = Text(self.window,width = 20,height =2,bg = "#000000",fg="green", font = "Calabri 13", padx = 5, pady = 5)
        self.textcons.place(relheight = 0.745, relwidth = 1,rely = 0.08)

        self.labelhead = Label(self.window,bg = "#000000",fg = "green", height = 80)
        self.labelhead.place(relheight = 0.5)

        self.labelBottom = Label(self.window,bg = "#000000",height = 80)
        self.labelBottom.place(relwidth = 1, rely = 0.825)

        self.entryMsg = Entry(self.labelBottom,bg = "#000000",fg = "green",font = "Helvetica 13")
        self.entryMsg.place(relwidth = 0.74,relheight = 0.06,rely = 0.008, relx = 0.011)
        self.entryMsg.focus()

        self.buttonMsg = Button(self.labelBottom,text = "Send",font = "Helvetica 10 bold",width = 20,bg = "#000000", fg = "green",command = lambda: self.sendButton(self.entryMsg.get()))
		
        self.buttonMsg.place(relx = 0.77,rely = 0.008,relheight = 0.06, relwidth = 0.22)
        
        self.textcons.config(cursor = "arrow")
		
        scrollbar = Scrollbar(self.textcons)

        scrollbar.place(relheight = 1, relx = 0.974)
		
        scrollbar.config(command = self.textcons.yview)
    
        self.textcons.config(state = DISABLED)


    def sendButton(self, msg):
        self.textcons.config(state = DISABLED)
        self.msg=msg
        self.entryMsg.delete(0, END)
        snd= Thread(target = self.write)
        snd.start()

    def show_message(self, message):
        self.textcons.config(state = NORMAL)
        self.textcons.insert(END, message+"\n\n")
        self.textcons.config(state = DISABLED)
        self.textcons.see(END)

    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                elif message == 'WA':
                    self.window.destroy()
                else:
                    self.show_message(message)
            except:
                print("An error occured!")
                client.close()
                break

    def write(self):
        self.textcons.config(state=DISABLED)
        while True:
            message = (f"{self.msg}")
            client.send(message.encode('utf-8'))
            self.show_message(message)	
            break

    
        


g = GUI()


# def write():
#     while True:
#         message = '{}'.format(input(""))
#         client.send(message.encode('utf-8'))







# recieve_thread = Thread(target=recieve)
# recieve_thread.start()
# # write_thread = Thread(target=write)
# write_thread.start()