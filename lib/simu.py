import curses

class MinitelSimu:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.cursor_x = 0
        self.cursor_y = 0
        self.inverted = False
        self.cls()  # Initialise avec un écran vidé

    def _print(self, text: str):
        for char in text:
            if self.cursor_x >= 40:
                self.cursor_x = 0
                self.cursor_y += 1
            if self.cursor_y >= 24:
                break

            # Déplace le curseur
            self.stdscr.addstr(self.cursor_y, self.cursor_x, char)

            # Inversion des couleurs si nécessaire
            if self.inverted:
                self.stdscr.attron(curses.A_REVERSE)
                self.stdscr.addstr(self.cursor_y, self.cursor_x, char)
                self.stdscr.attroff(curses.A_REVERSE)

            self.cursor_x += 1
        # Rafraîchir l'écran une fois que tout le texte est affiché
        self.stdscr.refresh()

    def inverse(self, on: bool = True):
        self.inverted = on

    def cls(self):
        """Efface l'écran et repositionne le curseur au début."""
        self.stdscr.clear()  # Efface l'écran
        self.stdscr.refresh()  # Rafraîchit l'affichage
        self.cursor_x = 0
        self.cursor_y = 0

    def pos(self, x: int, y: int):
        """Déplace le curseur à la position (x, y)."""
        self.cursor_x = max(0, min(39, x))
        self.cursor_y = max(0, min(23, y))
        self.stdscr.move(self.cursor_y, self.cursor_x)

    def vtab(self, n: int):
        """Déplace le curseur de n lignes vers le bas (vertical tab)."""
        self.cursor_y = max(0, min(23, self.cursor_y + n))
        self.stdscr.move(self.cursor_y, self.cursor_x)

    def _if(self) -> str:
        """Lecture d'une touche sans attendre Enter (Unix only)."""
        # Utiliser un délai pour ne pas bloquer l'exécution
        ch = None
        self.stdscr.timeout(10)  # Délai de 10 millisecondes
        try:
            ch = self.stdscr.getkey()  # Lit une touche si disponible
        except curses.error:
            # Pas de touche appuyée, on retourne None
            pass
        return ch

    def echo_off(self):
        """Désactive l'écho du clavier."""
        pass

def main(stdscr):
    simu = MinitelSimu(stdscr)  # Passe l'argument stdscr ici
    simu.cls()  # Clear screen

    # Affichage initial
    simu._print("Hello, World!")
    simu.pos(0, 2)
    simu.inverse(True)
    simu._print("This is inverted text!")

    # Attente d'une touche avant de quitter
    simu.stdscr.addstr(23, 0, "Press any key to exit...")
    simu.stdscr.refresh()

    # Boucle principale qui affiche sans bloquer
    while True:
        key = simu._if()  # Cherche une touche sans bloquer

        if key:
            simu._print(f"Key pressed: {key}")
            simu.pos(0, 0)  # Repositionner le curseur si nécessaire

        simu.stdscr.refresh()  # Toujours rafraîchir l'écran
