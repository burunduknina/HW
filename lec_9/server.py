import select
import socket
import re


class Server:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(" server will start on host : ", host)
        self.socket.bind((host, port))
        self.socket.listen(5)
        self.sockets = [self.socket]
        self.noname_sockets = []
        self.users = {}
        self.sockets_users = {}

    def new_socket(self, i_fds):
        clientsock, clientaddr = i_fds.accept()
        self.sockets.append(clientsock)
        login = clientsock.recv(1024).decode()
        print('connect from:', clientaddr)
        if self.users.get(login):
            clientsock.send(
                'Reject.'.encode())
            self.noname_sockets.append(clientsock)
        else:
            clientsock.send('Accepted.'.encode())
            self.users[login] = clientsock
            self.sockets_users[clientsock] = login
            for user_socket in self.sockets[1:]:
                user_socket.send(
                    f'{login} joined the chat'.encode())

    def set_login(self, data, fds):
        if self.users.get(data):
            fds.send(
                'Reject.'.encode())
        else:
            fds.send('Accepted.'.encode())
            self.users[data] = fds
            self.sockets_users[fds] = data
            for user_socket in self.sockets[1:]:
                user_socket.send(
                    f'{data} joined the chat'.encode())
            try:
                self.noname_sockets.remove(fds)
            except ValueError:
                fds.close()

    def close_socket(self, fds, login):
        fds.close()
        print(f'{login} quits.')
        try:
            self.sockets.remove(fds)
            del self.users[login]
            del self.sockets_users[fds]
            for user_socket in self.sockets[1:]:
                user_socket.send(
                    f'{login} left the chat'.encode())
        except ValueError:
            fds.close()

    def chat_message(self, data, login, outfds):
        newdata = f'\n{login}: {data}'
        if len(outfds) != 0:
            for fds in self.sockets[1:]:
                fds.send(newdata.encode())

    def private_message(self, data, login):
        recipient = re.match(r'>\w*>', data).group(
            0)[1:-1]
        client_socket = self.users[recipient]
        msg = data[len(recipient) + 2:]
        client_socket.send(
            f'\nPrivate messge from {login}: {msg}'.encode())

    def send_accounts_list(self, fds):
        newdata = 'Accounts: '
        for login in self.users.keys():
            newdata += login + ', '
        fds.send(newdata.encode())

    def parse_input(self, fds, outfds):
        data = fds.recv(1024).decode()
        if fds in self.noname_sockets:
            self.set_login(data, fds)
        else:
            login = self.sockets_users.get(fds)
            if not data:
                self.sockets.remove(fds)
            else:
                print(data)
                if data == 'q' or data == 'Q':
                    self.close_socket(fds, login)
                elif data == '?names':
                    self.send_accounts_list(fds)
                elif re.match(r'>\w*>', data):
                    self.private_message(data, login)
                else:
                    self.chat_message(data, login, outfds)

    def run_server(self):
        while 1:
            infds, outfds, errfds = select.select(
                self.sockets, self.sockets, [], 5)
            if len(infds) != 0:
                for fds in infds:
                    if fds is self.socket:
                        self.new_socket(fds)
                    else:
                        self.parse_input(fds, outfds)


if __name__ == '__main__':
    host = ''
    port = 10000
    server = Server(host, port)
    server.run_server()
