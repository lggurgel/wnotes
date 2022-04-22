import os
import pickle
import sys
import time
from pprint import pprint
from datetime import datetime, timedelta, timezone


FILENAME = "notes"

BANNER = """
 █████╗ ███╗   ██╗ █████╗     ███████╗    ██╗     ██╗   ██╗ ██████╗ █████╗ ███████╗
██╔══██╗████╗  ██║██╔══██╗    ██╔════╝    ██║     ██║   ██║██╔════╝██╔══██╗██╔════╝
███████║██╔██╗ ██║███████║    █████╗      ██║     ██║   ██║██║     ███████║███████╗
██╔══██║██║╚██╗██║██╔══██║    ██╔══╝      ██║     ██║   ██║██║     ██╔══██║╚════██║
██║  ██║██║ ╚████║██║  ██║    ███████╗    ███████╗╚██████╔╝╚██████╗██║  ██║███████║
╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝    ╚══════╝    ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝
                                                                                   
██████╗ ███████╗ ██████╗ █████╗ ██████╗  ██████╗ ███████╗                          
██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔════╝                          
██████╔╝█████╗  ██║     ███████║██║  ██║██║   ██║███████╗                          
██╔══██╗██╔══╝  ██║     ██╔══██║██║  ██║██║   ██║╚════██║                          
██║  ██║███████╗╚██████╗██║  ██║██████╔╝╚██████╔╝███████║                          
╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝                          
                                                                                   
██╗   ██╗ ██████╗    ██╗    ██████╗      ██╗██████╗ ███████╗████████╗ █████╗ ██╗   
██║   ██║██╔═████╗  ███║   ██╔═████╗    ██╔╝██╔══██╗██╔════╝╚══██╔══╝██╔══██╗╚██╗  
██║   ██║██║██╔██║  ╚██║   ██║██╔██║    ██║ ██████╔╝█████╗     ██║   ███████║ ██║  
╚██╗ ██╔╝████╔╝██║   ██║   ████╔╝██║    ██║ ██╔══██╗██╔══╝     ██║   ██╔══██║ ██║  
 ╚████╔╝ ╚██████╔╝██╗██║██╗╚██████╔╝    ╚██╗██████╔╝███████╗   ██║   ██║  ██║██╔╝  
"""

END_MESSAEGE = """

 ██████╗ ██████╗ ██████╗ ██╗ ██████╗  █████╗ ██████╗  ██████╗     ██████╗  ██████╗ ██████╗               
██╔═══██╗██╔══██╗██╔══██╗██║██╔════╝ ██╔══██╗██╔══██╗██╔═══██╗    ██╔══██╗██╔═══██╗██╔══██╗              
██║   ██║██████╔╝██████╔╝██║██║  ███╗███████║██║  ██║██║   ██║    ██████╔╝██║   ██║██████╔╝              
██║   ██║██╔══██╗██╔══██╗██║██║   ██║██╔══██║██║  ██║██║   ██║    ██╔═══╝ ██║   ██║██╔══██╗              
╚██████╔╝██████╔╝██║  ██║██║╚██████╔╝██║  ██║██████╔╝╚██████╔╝    ██║     ╚██████╔╝██║  ██║              
 ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝              
                                                                                                         
███████╗██╗   ██╗ █████╗     ███╗   ███╗███████╗███╗   ██╗███████╗ █████╗  ██████╗ ███████╗███╗   ███╗██╗
██╔════╝██║   ██║██╔══██╗    ████╗ ████║██╔════╝████╗  ██║██╔════╝██╔══██╗██╔════╝ ██╔════╝████╗ ████║██║
███████╗██║   ██║███████║    ██╔████╔██║█████╗  ██╔██╗ ██║███████╗███████║██║  ███╗█████╗  ██╔████╔██║██║
╚════██║██║   ██║██╔══██║    ██║╚██╔╝██║██╔══╝  ██║╚██╗██║╚════██║██╔══██║██║   ██║██╔══╝  ██║╚██╔╝██║╚═╝
███████║╚██████╔╝██║  ██║    ██║ ╚═╝ ██║███████╗██║ ╚████║███████║██║  ██║╚██████╔╝███████╗██║ ╚═╝ ██║██╗
╚══════╝ ╚═════╝ ╚═╝  ╚═╝    ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝
                                                                                                         

"""

SENTONEL_NAME = "ana"
SENTINEL_NOTE = "lucas"


def get_local_datetime() -> datetime:
    brazil_timezone = timezone(timedelta(hours=-3))
    local_datetime = datetime.now().astimezone(brazil_timezone)

    return local_datetime


def check_sentinel(input_note: dict):
    return input_note["name"] == SENTONEL_NAME and input_note["note"] == SENTINEL_NOTE


def print_notes() -> None:
    data = []
    with open(FILENAME, "rb") as fr:
        try:
            while True:
                data.append(pickle.load(fr))
        except EOFError:
            pass

    for note in data:
        print("Nome: {}".format(note["name"]))
        print("Mensagem: {}".format(note["note"]))

        just_time = note["created_at"].strftime("%H:%M")
        print("Hora da mensagem: {}".format(just_time))
        print("\n\n")


def read_note() -> dict:
    input_note = {}
    with open(FILENAME, "ab+") as outfile:
        name = input("\n\nDigite seu nome:\n")
        while not name:
            name = input()

        note = input(
            "\nDigite sua mensagem aos noivos e pressione Enter ↵ para enviar:\n"
        )
        while not note:
            note = input("")

        input_note = {"name": name, "note": note, "created_at": get_local_datetime()}

        if not check_sentinel(input_note):
            pickle.dump(input_note, outfile)

    return input_note


def main_process():
    os.system("clear")
    print(BANNER)

    input_note = read_note()

    if check_sentinel(input_note):
        os.system("clear")
        print_notes()
        sys.exit()
    else:

        print(END_MESSAEGE)

        time.sleep(2)
        os.system("clear")
        time.sleep(1)


if __name__ == "__main__":
    while True:
        main_process()
