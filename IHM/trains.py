import sys
from PyQt5 import QtWidgets, uic

class GearController(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Trains.ui', self)
        
        # Initialisation de l'emetteur Ivy
        self.ivy_emitter = None
        
        # Connecte le signal de la slider à la fonction update_trains_from_slider
        self.OnOffTrains.valueChanged.connect(self.update_trains_from_slider)

    # Fonction qui met à jour la position des trains en fonction de la valeur du slider
    def update_trains_from_slider(self):
        value = self.OnOffTrains.value()
        if 0 <= value <= 1:
            # Envoie la position des trains à Ivy
            if self.ivy_emitter:
                self.ivy_emitter(f"Position_train={value}")
                # Affiche la position des trains dans le terminal (simple test pour vérifier que la valeur est la bonne)
            if value == 0:
                print("UP")
            elif value == 1:
                print("DOWN")
            return value

    # Fonction qui met à jour la position du slider en fonction de la valeur passée en paramètre (venant du bus Ivy)
    def set_slider_value(self, value):
        if 0 <= value <= 1:
            self.OnOffTrains.setValue(value)
            print(f"Slider en position {value} (0=UP, 1=DOWN)")
        else:
            print("Valeur Invalide.")
    
    # Fonction qui initialise l'emetteur Ivy
    def set_ivy_emitter(self, ivy_emitter):
        self.ivy_emitter = ivy_emitter


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = GearController()
    window.show()
    sys.exit(app.exec_())
