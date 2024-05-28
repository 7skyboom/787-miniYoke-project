import sys
from PyQt5.QtWidgets import QApplication
from ivy.std_api import *
from main import MainController

def null_cb(*a):
    pass

def on_msg_volets(agent, *data):
    try:
        position_volets = int(data[0])  # Conversion de la position en entier
        print(f"Position volets depuis bus ivy: {position_volets}")
        vue_totale.signal_update_volets.emit(position_volets)  # Envoi du signal à la vue principale
    except ValueError:
        print("Mauvaise valeur (volets)")  # Affichage d'un message d'erreur si la valeur n'est pas un entier

def on_msg_trains(agent, *data):
    try:
        position_trains = int(data[0])  # Conversion de la position en entier
        print(f"Position trains depuis bus ivy: {position_trains}")
        vue_totale.signal_update_trains.emit(position_trains)  # Envoi du signal à la vue principale
    except ValueError:
        print(f"Mauvaise Valeur (trains)")  # Affichage d'un message d'erreur si la valeur n'est pas un entier

if __name__ == "__main__":
    app = QApplication(sys.argv)
    vue_totale = MainController()
    vue_totale.show()

    IvyInit("connectiontobus", "Ready", 0, null_cb, null_cb)  # Initialisation d'Ivy
    IvyStart("127.255.255.255:2010")  # Démarrage d'Ivy
    IvyBindMsg(on_msg_volets, '^Position_volet=(.*)')  # Liaison du message Ivy à la fonction on_msg_volets
    IvyBindMsg(on_msg_trains, '^Position_train=(.*)')  # Liaison du message Ivy à la fonction on_msg_trains

    vue_totale.set_ivy_emitter(IvySendMsg)  # Envoie IvySendMsg au ivy bus de la position du train et/ou des volets cpontrollés par la slider

    sys.exit(app.exec_())
