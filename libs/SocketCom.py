# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 15:22:02 2014

@author: hanno.flentje
"""


import socket
import re

def test():
    sock=SocketCom('192.168.137.2',4000)
    sock.openCom()
    sock.sendMessage('WLIST:SIZE?')
    ansr=sock.readMessage()
    print ansr

    msg=[]
    for i in xrange (1,int(ansr)+1):
       msg.append('WLIST:NAME? '+str(i))
    print msg
    sock.sendMessage(msg)
    wnames=sock.readMessage()
    print wnames

    LWNames = re.findall('"waveseq.*?"',wnames)
    print LWNames

    dlmsg=[]
    for name in LWNames:
        dlmsg.append('WLISt:WAVeform:DELete '+name)
    print dlmsg
    sock.sendMessage(dlmsg)

    sock.closeCom()


class SocketCom(object):
    """
    General Communication class for messages delimited by Delimiter and ended by  EndOfMessage to interface (Tektronix AWG) devices
    """
    def __init__(self, Ip, Port, Delimiter=';:', EndOfMessage='\n'):
        self.TCP_IP = Ip
        self.TCP_PORT = Port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.BUFFER_SIZE = 1024
        self.BUFFER_SIZE = 8*1024
        self.msgEnd=EndOfMessage
        self.delimiter=Delimiter

    def openCom(self):
        self.s.connect((self.TCP_IP, self.TCP_PORT))
        self.s.settimeout(300)

    def closeCom(self):
        self.s.close()

    def sendMessage(self,msg):
        if isinstance(msg, basestring):
            self.s.send(msg+self.msgEnd)
        else:
            try:
                fullMsg=''
                for msgPart in msg:
                    fullMsg=fullMsg+msgPart+self.delimiter
                fullMsg.rstrip(self.delimiter)
                self.s.send(fullMsg+self.msgEnd)
            except TypeError:
                print 'TypeError occourred on message text, please ensure that message is a string or a list of strings'


    def readMessage(self):
        cont=1
        dat=''
        while cont:
            dat=dat+self.s.recv(self.BUFFER_SIZE)
            if dat.endswith(self.msgEnd):
                cont=0
        return dat.rstrip(self.msgEnd)

if __name__=='__main__':
    test()