import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QMessageBox


class Minesweeper(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Minesweeper")

        self.rows = 10
        self.cols = 10

        grid_layout = QGridLayout()
        self.buttons = []
        self.mines = []
        self.clicked_buttons = set()
        self.game_over = False
        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                button = QPushButton()

                button.setFixedSize(30, 30)
                button.setStyleSheet("background-color: #CCCCCC")
                button.clicked.connect(self.button_clicked)
                button_row.append(button)
                grid_layout.addWidget(button, row, col)
            self.buttons.append(button_row)

        self.setLayout(grid_layout)

        self.place_mines()

        self.show()

    def place_mines(self):
        num_mines = 10

        mines = random.sample(range(self.rows * self.cols), num_mines)

        for mine in mines:
            row = mine // self.cols
            col = mine % self.cols
            self.mines.append((row, col))

    def button_clicked(self):
        clicked_button = self.sender()
        row, col = self.get_button_position(clicked_button)

        if self.game_over:
            return

        if (row, col) in self.mines:
            clicked_button.setStyleSheet("background-color: red")
            self.show_game_over_message()
        else:

            num_mines = self.count_neighbor_mines(row, col)

            if num_mines > 0:
                clicked_button.setText(str(num_mines))
            else:
                clicked_button.setText("0")
                self.expand_zeros(row, col)

            self.clicked_buttons.add((row, col))

            if self.check_winning_condition():
                self.show_game_won_message()

    def count_neighbor_mines(self, row, col):

        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbor_row = row + i
                neighbor_col = col + j
                if (
                        neighbor_row >= 0
                        and neighbor_row < self.rows
                        and neighbor_col >= 0
                        and neighbor_col < self.cols
                        and (neighbor_row, neighbor_col) in self.mines
                ):
                    count += 1
        return count

    def expand_zeros(self, row, col):

        self.clicked_buttons.add((row, col))
        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbor_row = row + i
                neighbor_col = col + j
                if (
                        neighbor_row >= 0
                        and neighbor_row < self.rows
                        and neighbor_col >= 0
                        and neighbor_col < self.cols
                        and (neighbor_row, neighbor_col) not in self.clicked_buttons
                ):
                    button = self.buttons[neighbor_row][neighbor_col]
                    button.click()

    def get_button_position(self, button):

        for i, button_row in enumerate(self.buttons):
            for j, btn in enumerate(button_row):
                if btn is button:
                    return i, j

    def check_winning_condition(self):
        total_buttons = self.rows * self.cols
        return len(self.clicked_buttons) == total_buttons - len(self.mines)

    def reveal_buttons(self):
        for button_row in self.buttons:
            for button in button_row:
                button.setEnabled(False)
                row, col = self.get_button_position(button)
                if (row, col) in self.mines:
                    button.setStyleSheet("background-color: red")
                else:
                    num_mines = self.count_neighbor_mines(row, col)
                    button.setText(str(num_mines))

    def show_game_over_message(self):
        self.game_over = True
        QMessageBox.about(self, "result", "Lost")
        self.reveal_buttons()

    def show_game_won_message(self):
        self.game_over = True
        QMessageBox.about(self, "result", "Win")
        self.reveal_buttons()

    def closeEvent(self, event):
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    minefield = Minesweeper()
    sys.exit(app.exec_())
