import socket
import threading
import tkinter


class ServerConnect:

    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self._socket.connect((host, port))


class MyUI:
    def __init__(self, socket):
        self.socket = socket
        self.is_active = True
        self.tk = tkinter.Tk()
        self.login_frame = tkinter.Frame(self.tk)
        self.login = tkinter.StringVar()
        self.login_field = tkinter.Entry(
            self.login_frame, textvariable=self.login)
        self.send_login = tkinter.Button(
            self.login_frame, text="Send", command=self.send_login)
        self.enter_login = tkinter.Label(
            self.login_frame, text="Enter username:")
        self.change_login = tkinter.Label(
            self.login_frame,
            text="This username is already in use. Please, select other"
                 " username."
        )
        self.messages_frame = tkinter.Frame(self.tk)
        self.msg = tkinter.StringVar()
        self.person = tkinter.StringVar()
        self.msg_list = tkinter.Listbox(
            self.messages_frame)
        self.scrollbar = tkinter.Scrollbar(
            self.messages_frame, command=self.msg_list.yview)
        self.person_lbl = tkinter.Label(
            self.messages_frame,
            text="For private message enter username here:"
        )
        self.entry_field = tkinter.Entry(
            self.messages_frame, textvariable=self.msg)
        self.entry_lbl = tkinter.Label(
            self.messages_frame, text="Enter your message here:")
        self.person_field = tkinter.Entry(
            self.messages_frame, textvariable=self.person)
        self.send_button = tkinter.Button(
            self.messages_frame, text="Send", command=self.send_msg)
        self.users_button = tkinter.Button(
            self.messages_frame, text="Users", command=self.users)
        self.quit_button = tkinter.Button(
            self.messages_frame, text="Quit", command=self.quit_chat)

    def configure_window(self):
        self.tk.title('My chat')
        self.tk.geometry('900x800')

    def create_login_frame(self):
        self.login.set('')
        self.login_frame.pack(side=tkinter.TOP, fill='x', expand='true')
        self.enter_login.pack(side=tkinter.TOP)
        self.login_field.pack(side=tkinter.TOP)
        self.send_login.pack(side=tkinter.TOP)
        tkinter.mainloop()

    def create_chat_frame(self):
        self.login_frame.destroy()
        self.person.set('')
        self.entry_field.bind("<Return>", self.send_msg)
        self.messages_frame.place(x=10, y=10, relwidth=0.99, relheight=0.99)
        self.msg_list.place(anchor='nw', relwidth=0.99, relheight=0.8)
        self.scrollbar.place(x=865, y=2, width=15, height=632)
        self.person_lbl.place(x=4, y=640)
        self.person_field.place(x=230, y=640, width=150)
        self.entry_field.place(x=230, y=670, width=600)
        self.entry_lbl.place(x=4, y=670)
        self.send_button.place(x=840, y=667)
        self.quit_button.place(x=500, y=730)
        self.users_button.place(x=400, y=730)
        self.msg_list.config(yscrollcommand=self.scrollbar.set)
        self.tk.protocol("WM_DELETE_WINDOW", self.close_window)


class LoginMixin:

    def login_chat(self):
        self.create_login_frame()

    def send_login(self):
        data = self.login.get()
        self.login.set('')
        self.socket.send(data.encode())
        if data == 'q' or data == 'Q':
            self.socket.close()
            self.tk.quit()
        res = self.socket.recv(1024).decode()
        if 'Reject.' in res:
            self.change_login.pack(side=tkinter.TOP)
        elif 'Accepted.' in res:
            self.chat()


class ChatMixin:
    def chat(self):
        self.create_chat_frame()
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        tkinter.mainloop()

    def receive(self):
        while True:
            try:
                data = self.socket.recv(1024).decode()
                self.msg_list.insert(tkinter.END, data)
            except OSError:
                break

    def send_msg(self):
        data = self.msg.get()
        pr_person = self.person.get()
        if pr_person:
            data = f'>{pr_person}>{data}'
        self.msg.set('')
        self.socket.send(data.encode())
        if data == 'q' or data == 'Q':
            self.socket.close()

    def quit_chat(self):
        if self.is_active:
            self.msg.set("q")
            self.send_msg()
            self.is_active = False
            self.entry_field.destroy()
        else:
            self.tk.destroy()

    def close_window(self):
        if self.is_active:
            self.quit_chat()
        self.tk.destroy()

    def users(self):
        self.socket.send('?names'.encode())


class MyChat(LoginMixin, ChatMixin, MyUI):
    pass


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 10000
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((host, port))
    my_chat = MyChat(socket)
    my_chat.configure_window()
    my_chat.login_chat()
