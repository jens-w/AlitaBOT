#!/usr/bin/python3
import socket
from datetime import datetime
import threading
import importlib

import AlitaCommands

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "irc.quakenet.org"
networkname = "quakenet"
channel = "#Alita"
botnick = "AlitaB"
adminname = "nha"
exitcode = "bye " + botnick
stop = False
connected = False


def connect():
    print(timestamp("connecting"))
    ircsock.connect((server, 6667))
    readmessages = threading.Thread(target=readmsg, daemon=True)
    readmessages.start()
    print(timestamp("send USER"))
    ircsock.send(bytes("USER " + botnick + " " + botnick + " " + botnick + " " + botnick + "\n", "UTF-8"))
    print(timestamp("send NICK"))
    ircsock.send(bytes("NICK " + botnick + "\n", "UTF-8"))


def timestamp(message):
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " " + message


def joinchan(chan):
    print(timestamp("joining channel"))
    ircsock.send(bytes("JOIN " + chan + "\n", "UTF-8"))


def ping(message):
    print(timestamp("PONG " + message))
    ircsock.send(bytes("PONG " + message + "\n", "UTF-8"))


def parse_servermsg(msg):
    msg = msg.replace(":", "", 1)
    host = ""
    reply_or_cmd = ""
    nick = ""

    if msg.find(" ") != -1:
        index = msg.index(" ")
        host = msg[0:index]
        msg = msg[index + 1:len(msg)]

    if msg.find(" ") != -1:
        index = msg.index(" ")
        reply_or_cmd = msg[0:index]
        msg = msg[index + 1:len(msg)]

    if msg.find(" ") != -1:
        print(msg)
        index = msg.index(" ")
        nick = msg[0:index]
        msg = msg[index + 1:len(msg)]

    if msg.startswith(" "):
        msg = msg.replace(" ", "", 1)

    if msg.startswith(":"):
        msg = msg.replace(":", "", 1)

    if reply_or_cmd == "001":
        global connected
        connected = True

    if reply_or_cmd == "MODE":
        print(timestamp("mode: " + msg))
        return

    elif reply_or_cmd == "NOTICE":
        print(timestamp("notice: " + msg))
        return

    print(timestamp(msg))


def parsemsg(msg):
    if msg.find("PING :") != -1:
        message = msg.split(':', 1)[1]
        ping(message)
        return

    if msg.find("PRIVMSG") != -1:
        name = msg.split('!', 1)[0][1:]
        message = msg.split('PRIVMSG', 1)[1].split(':', 1)[1]

        if name.lower() == adminname.lower() and message.rstrip() == "!reload":
            importlib.reload(AlitaCommands)

        if name.lower() == adminname.lower() and message.rstrip() == exitcode:
            global stop
            stop = True
            return

        if message.find('Hi '.lower() + botnick) != -1:
            sendmsg("Hello " + name + "!")
            return

        if message[:5].find('.tell') != -1:
            target = message.split(' ', 1)[1]

            if target.find(' ') != -1:
                message = target.split(' ', 1)[1]
                target = target.split(' ')[0]
            else:
                target = name
                message = "Could not parse. The message should be in the format of ‘.tell [target] [message]’ to " \
                          "work properly. "

            sendmsg(message, target)

    if msg.startswith(":"):
        parse_servermsg(msg)
        return

    if msg.find("NOTICE AUTH:") != -1:
        msg = msg.split(':', 1)[1]

    print("\t\t" + timestamp(msg))


def readmsg():
    while 1:
        msg = ircsock.recv(2048).decode("UTF-8")

        if (msg.find("\n")) or (msg.find("\r")):
            splitlines = msg.splitlines()

            for line in splitlines:
                parsemsg(line)

        else:
            msg = msg.strip('\n\r')
            parsemsg(msg)


def sendmsg(msg, target=channel):
    print(timestamp("sending " + "PRIVMSG " + target + " :" + msg + "\n"))
    ircsock.send(bytes("PRIVMSG " + target + " :" + msg + "\n", "UTF-8"))


def main():
    connect()

    while not connected:
        going = "yes"

    joinchan(channel)

    while not stop:
        going = "yes"

    sendmsg("oh...okay. :'(")
    print(timestamp("quitting"))
    ircsock.send(bytes("QUIT \n", "UTF-8"))
    return


main()
