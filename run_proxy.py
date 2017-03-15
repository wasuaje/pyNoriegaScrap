#!/usr/bin/env python

# No data validation or elegant program tricks ... What do you want for
# free and 5 minutes? :)

import socket
import sys

proxyAddr = "172.30.115.251"
proxyPort = 3128
remoteAddr = "mail.wasuaje.com"
remotePort = 25
localhostPort = 8080

pSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pSock.connect((proxyAddr, proxyPort))
print(socket.gethostbyname(socket.gethostname()))
pSock.send(
    b"CONNECT %s:%s HTTP/1.1\r\nHost: %s:  %s \r\n\r\n"
)


sSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sSock.bind(("", localhostPort))

sSock.listen(1)
(cliSock, cliAddr) = sSock.accept()
print("Accepted connection from %s" % str(cliAddr))

while(cliSock):
    cliSock.send(pSock.recv(1024))
    pSock.send(cliSock.recv(1024))

pSock.close()
sSock.close()
