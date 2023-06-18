import socket
from threading import Thread
import time

import os
import pickle

import cv2
import numpy as np
import pandas as pd

from action import Action
from environment import Environment


# ******************************************************************************
# Settings
# ******************************************************************************
SRV_IP = "0.0.0.0"
SRV_PORT = 1415
BUFF_SIZE = 1024
LBR_IP = "10.84.57.105"

ai_state = 0
ai_sequence = ""
ai_config = ""
moves_string = ""
# Bewegungs String muss angepasst werden
# TEST
#moves_string = ("rdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuurrrrr" )


class interface:
    def make_xml(self, target, given):
        input = []
        row = 0
        ret = ""
        record = "<msg> \n\t<target>Record</target>\n"  # target == 1
        wait = "<msg> \n\t<target>Wait</target>\n"  # target == 2
        start = "<msg> \n\t<target>Start</target>\n"  # target == 3
        end = "<msg> \n\t<target>End</target>\n"  # target == 4

        before = ""
        count = 1
        short = ""
        for i in given:
            if before == "":
                before = i

            if before == i:
                count += 1
            else:
                if count == 1:
                    count = ""
                short += before + str(count) + before
                before = i
                count = 1
        c = 0
        strary = ""
        for i in short:
            if c == 49:
                input.append(strary)
                c = 0
                strary = ""

            strary += i
            c += 1
        input.append(strary)

        with open("Hotwire.xml", "w+") as file:
            if target == 1:
                ret += record
            elif target == 2:
                ret += wait
            elif target == 3:
                ret += start
                for i in input:
                    frontstr = "\t\t<s%02i>" % row
                    backstr = "</s%02i>\n" % row
                    ret += frontstr + i + backstr
                    row += 1
                    if row > 19:
                        break
                ret += "\t</seq>\n"
            elif target == 4:
                ret += end
            else:
                print("Wrong Target: Invalid size of target")

            ret += "\t</msg>"
            file.write(ret)
        return ret


# ******************************************************************************
# Common methods and functions
# ******************************************************************************
def str_to_bytes(s: str):
    """Convert string into bytes.
    :param s: String to convert.
    :return: Bytes representation of string s.
    """
    return bytes(s, "utf-8")


def bytes_to_str(b: bytes):
    """Convert bytes into string.
    :param b: Bytes to convert.
    :return: String representation of bytes b.
    """
    return str(b, "utf-8")


# ******************************************************************************
# TCP-client's thread
# ******************************************************************************
class ClientThread(Thread):
    """TCP-client's thread."""

    def __init__(self, conn, ip, port, buff_size):
        Thread.__init__(self)
        self.conn = conn
        self.ip = ip
        self.port = port
        self.buff_size = buff_size
        print("\nCONNECTED    | Client's IP: {}:{}".format(ip, port))

    def run(self):
        global ai_state
        global ai_sequence
        global ai_config
        while True:
            try:
                data = self.conn.recv(self.buff_size)
                if not data:
                    print("LBR_DISCONNECT |")
                    break
                else:
                    print("RCV_FROM_LBR | {}".format(data))
                    data = bytes_to_str(data)
                    to_send = ""
                    if data == "HotWireStarted":
                        to_send = interface.make_xml(self, 1, "")
                    elif data == "OnRecord":
                        if ai_state == 0:
                            # AI thread takes photo and calculates movement path
                            ai_state = 1
                            to_send = interface.make_xml(self, 2, "")  # wait
                        elif ai_state == 1:
                            # AI still calculates the movement path
                            to_send = interface.make_xml(self, 2, "")  # wait
                        elif ai_state == 2:
                            # AI is ready with the calculation and generates motion string
                            moves_string = ai_test.get_moves_string()  # Get the moves_string from AI
                            to_send = interface.make_xml(self, 3, moves_string)  # start
                            ai_state = 0
                    elif data == "NoSeq":
                        to_send = interface.make_xml(self, 3, moves_string)  # start
                    elif data == "Finished":
                        to_send = interface.make_xml(self, 4, "")  # end
                    else:
                        to_send = ""

                    if to_send != "":
                        self.conn.send(str_to_bytes(to_send))
                        print("SENT_TO_LBR  | {}".format(to_send))
            except IOError as err:
                print("IO error: {0}".format(err))
                break
        print("DISCONNECTED | Client's IP: {}:{}".format(self.ip, self.port))


# ******************************************************************************
# Test AI class and thread
# ******************************************************************************
class AiTestClass:
    def __init__(self):
        self.seq = ""
        self.config = ""

    def take_photo(self):
        photo = str(b"\xF0\x9F\x93\xB8", "utf-8")
        print(f"\nAI take the {photo}.\n")
        time.sleep(5)

    
    def solver(self):
        execute_best = ExecuteBest()
        execute_best.execute()
        self.best_actions = ''.join(execute_best.all_actions)
        print("AI solver hat die besten Aktionsschritte ausgewählt.")
        time.sleep(15)

        # Generate moves_string based on the solver result
        self.moves_string = self.best_actions

    def get_moves_string(self):
        return self.moves_string


class AiThread(Thread):
    def __init__(self, ai):
        Thread.__init__(self)
        self.ai = ai

    def run(self):
        global ai_state
        global ai_sequence
        global ai_config
        ai_sequence = ""
        ai_config = ""
        while True:
            if ai_state == 1:
                self.ai.take_photo()
                self.ai.solver()
                ai_sequence = self.ai.seq
                ai_config = self.ai.config
                ai_state = 2


# ******************************************************************************
# Multithreaded python server: TCP-server socket program
# ******************************************************************************
def server():
    """Multithreaded python server: TCP-server socket program."""
    clients = []

    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_server.bind((SRV_IP, SRV_PORT))
        print("### SRV: started **************************************************")
        print(
            "### SRV: waiting for connections from TCP clients on port-no: ", SRV_PORT
        )
        srv_run = True
    except socket.error as err:
        print("### SRV: some errors while starting:\n", err)
        srv_run = False
        exit(1)

    while srv_run:
        tcp_server.listen(1)
        (conn, (ip, port)) = tcp_server.accept()
        if ip == LBR_IP:  # only KUKA LBR4+ allowed
            new_client = ClientThread(conn, ip, port, BUFF_SIZE)
            new_client.start()
            clients.append(new_client)

    for item in clients:
        item.join()


def ai():
    ai_test = AiTestClass()
    ai_thread = AiThread(ai_test)
    ai_thread.start()


# ******************************************************************************
# Main program
# ******************************************************************************
if __name__ == "__main__":
    ai()
    server()
