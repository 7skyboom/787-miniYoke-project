import sys
from PyQt5 import QtWidgets, QtCore
from trains import GearController
from volets import FlapsController

class MainController(QtWidgets.QWidget):
    
    # cree un signal pour mettre a jour les volets et les trains
    signal_update_volets = QtCore.pyqtSignal(int)
    signal_update_trains = QtCore.pyqtSignal(int)

    # cree une classe principale qui contient les deux controleurs
    def __init__(self, parent=None):
        super(MainController, self).__init__(parent)
        
        
        # cree les deux controleurs (les recupères dans les fichiers trains.py et volets.py)
        self.gear_controller = GearController()
        self.flaps_controller = FlapsController()
        
        #les ajoute dans un layout horizontal (moche mais bon)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.flaps_controller)
        layout.addWidget(self.gear_controller)
        self.setLayout(layout)
        
        #connecte les signaux des controleurs aux signaux de la classe 
        self.signal_update_volets.connect(self.flaps_controller.set_slider_value) #connecte le signal de la classe au volets
        self.signal_update_trains.connect(self.gear_controller.set_slider_value) #connecte le signal de la classe au trains
        
        
        self.ivy_emitter = None
        
    #initialise les emetteurs ivy
    def set_ivy_emitter(self, ivy_emitter):
        self.ivy_emitter = ivy_emitter
        self.gear_controller.set_ivy_emitter(ivy_emitter)
        self.flaps_controller.set_ivy_emitter(ivy_emitter)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainController()
    main_window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
