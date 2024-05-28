import sys
from PyQt5 import QtWidgets, uic

class FlapsController(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Volets.ui', self)
        
        # Initialisation de l'emetteur Ivy
        self.ivy_emitter = None

        # Connecte le signal de la slider à la fonction update_volets_from_slider
        self.sliderVolets.valueChanged.connect(self.update_volets_from_slider)

    # Fonction qui met à jour la position des volets en fonction de la valeur du slider
    def update_volets_from_slider(self):
        value = self.sliderVolets.value()
        if 0 <= value <= 3: # Vérifie que la valeur est bien comprise entre 0 et 3
            # Envoie la position des volets à Ivy
            if self.ivy_emitter:
                self.ivy_emitter(f"Position_volet={value}") # Envoie la position des volets à Ivy
            print(f"Position {value}")
            return value

    def set_slider_value(self, value): # Fonction qui met à jour la position du slider en fonction de la valeur passée en paramètre (venant du bus Ivy)
        if 0 <= value <= 3: # Vérifie que la valeur est bien comprise entre 0 et 3
            self.sliderVolets.setValue(value) # Met à jour la position du slider
            print(f"Slider en position {value}") # Affiche la position des volets dans le terminal (simple test pour vérifier que la valeur est la bonne)
        else:
            print("Valeur invalide.")
            
    # Fonction qui initialise l'emetteur Ivy
    def set_ivy_emitter(self, ivy_emitter):
        self.ivy_emitter = ivy_emitter


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = FlapsController()
    window.show()
    sys.exit(app.exec_())
