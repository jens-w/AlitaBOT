#!/usr/bin/python3
# coding=utf-8

# my personal IRC bot, only meant to run on one channel, on one network (in my case: #Alita on QuakeNet

import socket
from datetime import datetime
import threading
import importlib
import time
from queue import Queue

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
queue = Queue(maxsize=5)


# connect to the server and start reading messages
def connect():
    print(timestamp("connecting"))
    ircsock.connect((server, 6667))

    # continuously read messages
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


# parse server messages/replies
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

    if reply_or_cmd == "221":
        print(timestamp("user mode: " + msg))

    if (reply_or_cmd == "372") or (reply_or_cmd == "374") or (reply_or_cmd == "375") or (reply_or_cmd == "376"):
        return

    if reply_or_cmd == "MODE":
        print(timestamp("mode: " + msg))

        return

    elif reply_or_cmd == "NOTICE":
        print(timestamp("notice: " + msg))

        return

    print(timestamp(msg))


# parse all messages from server
def parsemsg(msg):
    if msg.find("PING :") != -1:
        message = msg.split(':', 1)[1]
        ping(message)

        return

    if msg.find("PRIVMSG") != -1:
        name = msg.split('!', 1)[0][1:]
        message = msg.split('PRIVMSG', 1)[1].split(':', 1)[1]

        if name.lower() == adminname.lower() and message.rstrip() == "!reload":
            print(timestamp(msg))
            print(timestamp("reloading commands"))
            importlib.reload(AlitaCommands)

            return

        if name.lower() == adminname.lower() and message.rstrip() == exitcode:
            global stop
            stop = True

            return

        for x in AlitaCommands.command_prefix:
            if message.startswith(x):
                if message.find(" ") != -1:
                    command = message[1:message.index(" ")]
                    text = message[message.index(" "):len(message)]
                else:
                    command = message[1:len(message)]
                    text = ""

                print(timestamp(name + " : " + message))

                if command in AlitaCommands.commands:
                    if text != "" and text is not None:
                        reply = AlitaCommands.commands[command](name, text)
                    else:
                        reply = AlitaCommands.commands[command](name)

                    if reply != "" and reply is not None:
                        add_to_queue(reply)

                return

        if message.find('Hi '.lower() + botnick) != -1:
            add_to_queue("Hello " + name + "!")

            return

    # these should be server replies
    if msg.startswith(":"):
        parse_servermsg(msg)

        return

    if msg.find("NOTICE AUTH :") != -1:
        msg = msg.replace("NOTICE AUTH :", "", 1)
        print(timestamp(msg))


def readmsg():
    while 1:
        # noinspection PyBroadException
        try:
            msg = ircsock.recv(2048).decode("UTF-8")

            # multiline messages
            if (msg.find("\n")) or (msg.find("\r")):
                splitlines = msg.splitlines()

                for line in splitlines:
                    parsemsg(line)

            # single line messages
            else:
                msg = msg.strip('\n\r')
                parsemsg(msg)

        # ignore exceptions so we can keep processing
        except Exception:
            pass


def add_to_queue(msg, target=None):
    # [msg, target] is an unordered list, because we want to retain the order for processing
    queue.put([msg, target])


def sendmsg(msg, target=channel):
    print(timestamp("sending " + "PRIVMSG " + target + " :" + msg))
    ircsock.send(bytes("PRIVMSG " + target + " :" + msg + "\n", "UTF-8"))


def parse_queue():
    while 1:
        # noinspection PyBroadException
        try:
            if queue.qsize() > 0:
                queue_item = queue.get()
                msg = queue_item[0]

                if len(queue_item) > 1 and queue_item[1] is not None:
                    target = queue_item[1]
                    sendmsg(msg, target)
                    time.sleep(2)

                else:
                    sendmsg(msg)
                    time.sleep(2)

        # ignore exceptions so we can keep processing
        except Exception:
            pass


def main():
    connect()

    while not connected:
        pass

    # parse send queue
    parse_send_queue = threading.Thread(target=parse_queue, daemon=True)
    parse_send_queue.start()

    time.sleep(1)
    joinchan(channel)

    while not stop:
        pass

    sendmsg("oh...okay. :'(")
    print(timestamp("quitting"))
    ircsock.send(bytes("QUIT \n", "UTF-8"))

    return


main()
