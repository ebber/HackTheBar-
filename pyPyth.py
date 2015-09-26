import socket
import sys
import time

disconnectCode = "0\n"
beerLockedCode="lock\n"
beerUnlockedCode="unlo\n"

pricePL=1;

users = {};


#We are 172.17.46.16
# Create a TCP/IP socket
#user tag = 5 digits

#get the ip addr
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
server_name = s.getsockname()[0]
s.close()

#server_name = "172.17.46.16"
server_port_base = 1338
server_port_inc =0;
server_port = server_port_base + server_port_inc
server_address = (server_name, server_port)
beerLocked=0
beerFlowing=0;
cash=0;

def lock_beer(connection):
    #connection.sendall("0\n")
    print "Machine locked"
    beerLocked=1;

def unlock_beer(data):
    if  not users.has_key(data):
        users[data]=0;

    users[data]=users[data]+pricePL;
    print "Machine unlocked"
    beerLocked=0;


def setUpServer():
    server_address = (server_name, server_port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    print >>sys.stderr, ' %s  %s' % server_address

    # Bind the socket to the port
    sock.bind(server_address)
    sock.listen(1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        cash=0;
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(10)
            print >>sys.stderr, 'received "%s"' % data

            if 5 == len(data)-1: #we got a valid uiud
                #if  not users.has_key(str(data)):
                #    users[data]=0;
                unlock_beer(str(data));
                connection.send(str(users[str(data)]))
                if beerLocked:
                    connection.send(beerUnlockedCode)
                else: 
                    connection.send(str(cash));
                    cash=cash+2;

            elif disconnectCode == data:
                connection.send(beerLockedCode)
                connection.sendall("0 \n")
                lock_beer(connection);
                connection.shutdown(2)
                connection.close()
                #sock.shutdown(socket.SHUT_RDWR)
                #sock.close()

                break;
                
            elif data:
                print >>sys.stderr, 'asking for good data'
                connection.send("invd")
                print len(data)

            else:
                lock_beer(connection);
                connection.send(beerLockedCode)
                connection.sendall("0\n")
                print >>sys.stderr, 'no more data from', client_address
                # Clean up the connection
                server_port_inc=server_port_inc+1 % 3
                connection.shutdown(socket.SHUT_RDWR)
                connection.close()
                #sock.shutdown(socket.SHUT_RDWR)
                #sock.close()
                break
    #except Exception, e:
     #   raise e
            
    finally:
        lock_beer(connection);
        # Clean up the connection
        #server_port_inc = (server_port_inc+1) % 3
        #connection.shutdown(socket.SHUT_RDWR)
        #connection.close()
        #sock.shutdown(socket.SHUT_RDWR)
        #sock.close()



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
