#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021

@author: bing
"""

# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from chat_utils import *
# Sylvia: import messagebox to display message boxes in a GUI application
from tkinter import messagebox
import json
# Sylvia: import the xlrd module to read data from Excel files, xlwt to write data to Excel files, and xlutils to work with Excel files, such as copying sheets between workbooks
import xlrd
import xlwt
from xlutils.copy import copy

# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""

    def login(self):
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width = False, 
                             height = False)
        self.login.configure(width = 400,
                             height = 300)
        # create a Label
        self.pls = Label(self.login, 
                       text = "Please login to continue",
                       justify = CENTER, 
                       font = "Helvetica 14 bold")
          
        self.pls.place(relheight = 0.15,
                       relx = 0.2, 
                       rely = 0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text = "Name: ",
                               font = "Helvetica 12")
          
        self.labelName.place(relheight = 0.2,
                             relx = 0.1, 
                             rely = 0.2)
          
        # create a entry box for 
        # tyoing the message
        self.entryName = Entry(self.login, 
                             font = "Helvetica 14")
          
        self.entryName.place(relwidth = 0.4, 
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.2)
          
        # set the focus of the curser
        self.entryName.focus()

        # create a Entry widget for
        # typing the password
        self.labelPassword = Label(self.login,
                                   text = "Password: ",
                                   font = "Helvetica 12")

        self.labelPassword.place(relheight = 0.2,
                                 relx = 0.1,
                                 rely = 0.4)

        self.entryPassword = Entry(self.login,
                                   font = "Helvetica 14",
                                   show = '*')

        self.entryPassword.place(relwidth = 0.4,
                                 relheight = 0.12,
                                 relx = 0.35,
                                 rely = 0.4)
        # create a Continue Button 
        # along with action
        self.go = Button(self.login,
                         text = "CONTINUE", 
                         font = "Helvetica 14 bold", 
                         # command = lambda: self.goAhead(self.entryName.get()))
                         command = self.checkLogin)

        self.go.place(relx = 0.35,
                      rely = 0.55)

         # Sylvia: create a sign up button
        self.signup = Button(self.login,
                             text = "SIGN UP",
                             font = "Helvetica 14 bold",
                             command = self.register)
        self.signup.place(relx = 0.35,
                          rely = 0.7)

        self.users = {}  # Sylvia: dictionary to store username and password

        self.Window.mainloop()

    # Sylvia: handle the login functionality
    def checkLogin(self):
        username = self.entryName.get()
        password = self.entryPassword.get()

        workbook = xlrd.open_workbook('users.xls')
        worksheet = workbook.sheet_by_name('Sheet1')

        for i in range(1, worksheet.nrows):
            row = worksheet.row_values(i)
            if row[0] == username and row[1] == password:
                messagebox.showinfo("Success", "Login successful!")

                # Add code to open the main window here
                self.goAhead(username)
                self.login.destroy()
                self.Window.mainloop()
                break
        else:
            messagebox.showerror("Error", "Invalid username or password")

    # Sylvia: create a new window for user registration 
    
    def register(self):
        # create a new window
        self.register = Toplevel()
        self.register.title("Register")
        self.register.resizable(width=False, height=False)
        self.register.configure(width=400, height=300)

        # create a Label
        self.pls = Label(self.register, text="Please enter details below", justify=CENTER, font="Helvetica 14 bold")
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        # create a Label for username
        self.labelName = Label(self.register, text="Username: ", font="Helvetica 12")
        self.labelName.place(relheight=0.2, relx=0.1, rely=0.2)

        # create a entry box for username
        self.entryName = Entry(self.register, font="Helvetica 14")
        self.entryName.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)

        # create a Label for password
        self.labelPass = Label(self.register, text="Password: ", font="Helvetica 12")
        self.labelPass.place(relheight=0.2, relx=0.1, rely=0.4)

        # create a entry box for password
        self.entryPass = Entry(self.register, font="Helvetica 14", show="*")
        self.entryPass.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.4)

        # create a button to register
        self.submit = Button(self.register, text="Register", font="Helvetica 14 bold", command=self.register_user)
        self.submit.place(relx=0.4, rely=0.7)

        self.Window.mainloop()

    def register_user(self):
        # get username and password from entry boxes
        username = self.entryName.get()
        password = self.entryPass.get()
        workbook = xlrd.open_workbook(r'users.xls')
        worksheet = workbook.sheet_by_name('Sheet1')
        # # check if username already exists in xls
        for i in range(1, worksheet.nrows):
            row = worksheet.row_values(i)
            if row[0] == username:
                messagebox.showerror("Error", "Username already exists!")
                return
                # if password == row[1]:

        # insert new user into xls
        workbook_copy = copy(workbook)
        worksheet_copy = workbook_copy.get_sheet(0)

        # Get the last row number in the worksheet
        last_row_num = worksheet.nrows

        # Write the values to the last row
        worksheet_copy.write(last_row_num, 0, username)
        worksheet_copy.write(last_row_num, 1, password)

        # Save the workbook
        workbook_copy.save('users.xls')

        # close register window and show success message
        self.register.destroy()
        messagebox.showinfo("Success", "Registration successful!")

    def goAhead(self, name):
        if len(name) > 0:
            msg = json.dumps({"action":"login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state = NORMAL)
                # self.textCons.insert(END, "hello" +"\n\n")
                self.textCons.insert(END, menu +"\n\n")
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)
                # while True:
                #     self.proc()
        # the thread to receive messages
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()
  
    # The main layout of the chat
    def layout(self,name):
        
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = "#17202A")
        self.labelHead = Label(self.Window,
                             bg = "#17202A", 
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
          
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#ABB2B9")
          
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
          
        self.textCons = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14", 
                             padx = 5,
                             pady = 5)
          
        self.textCons.place(relheight = 0.745,
                            relwidth = 1, 
                            rely = 0.08)
          
        self.labelBottom = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 80)
          
        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)
          
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
          
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
          
        self.entryMsg.focus()
          
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))
          
        self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06, 
                             relwidth = 0.22)
          
        self.textCons.config(cursor = "arrow")
          
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
          
        # place the scroll bar 
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
          
        scrollbar.config(command = self.textCons.yview)
          
        self.textCons.config(state = DISABLED)
  
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)

    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            # print(self.msg)
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                self.system_msg += self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state = NORMAL)
                self.textCons.insert(END, self.system_msg +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)

    def run(self):
        self.login()
# create a GUI class object
if __name__ == "__main__": 
    g = GUI()