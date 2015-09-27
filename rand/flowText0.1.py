import socket
import sys
import time

disconnectCode = "0\n"

users = {};


#We are 172.17.46.16
# Create a TCP/IP socket
#user tag = 5 digits

#get the ip addr
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
server_name = s.getsockname()[0]
s.close()

server_name = "172.17.46.16"
server_port_base = 1338
server_port_inc =0;
server_port = server_port_base + server_port_inc
server_address = (server_name, server_port)

def lock_beer(connection):
    #connection.sendall("0\n")
    print "Machine locked"

def unlock_beer(code):
    users[code]=0;
    print "Machine unlocked"


def setUpServer():
    server_address = (server_name, server_port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    print >>sys.stderr, ' %s  %s' % server_address

    # Bind the socket to the port
    sock.bind(server_address)
    sock.listen(1)
    #sock.allow_reuse_address(True)

    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(10)
            print >>sys.stderr, 'received "%s"' % data

            if 5 == len(data)-1: #we got a valid uiud
                unlock_beer(data);
                connection.send("beer unlocked \n")

            elif disconnectCode == data:
                connection.send("beer locked \n")
                connection.sendall("0 \n")
                lock_beer(connection);
                connection.shutdown(socket.SHUT_RDWR)
                connection.close()
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()

                break;
                
            elif data:
                print >>sys.stderr, 'asking for good data'
                connection.send(data)
                print len(data)

            else:
                lock_beer(connection);
                connection.send("beer locked\n")
                connection.sendall("0\n")
                print >>sys.stderr, 'no more data from', client_address
                # Clean up the connection
                server_port_inc=server_port_inc+1 % 3
                connection.shutdown(socket.SHUT_RDWR)
                connection.close()
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
                break
            
    finally:
        # Clean up the connection
        server_port_inc = (server_port_inc+1) % 3
        connection.shutdown(socket.SHUT_RDWR)
        connection.close()
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()

while True:
    try:
        server_port=server_port_base + server_port_inc
        setUpServer();
    except:
        print "we are erroring out"
        print server_port
        server_port_inc = (server_port_inc+1)%3
        server_port = server_port_inc % 3 + server_port_base
        print server_port

        time.sleep(1);
    finally:
        time.sleep(1)
        pass;
