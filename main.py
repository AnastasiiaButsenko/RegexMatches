import os
import sys
import program
import rules
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
import re
from d import rules_dictionary, set_dictionary


class Rules(QtWidgets.QMainWindow, rules.Ui_Rules):
    def __init__(self):
        super(Rules, self).__init__()
        self.setupUi(self)

        for rule in rules_dictionary:
            self.textBrowser.append(str(rule + '  ->  {}'.format(rules_dictionary.get(rule))))

        for rule in set_dictionary:
            self.textBrowser.append(str(rule + '  ->  {}'.format(set_dictionary.get(rule))))


class MainWindow(QtWidgets.QMainWindow, program.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.rules = None

        self.button_rules.clicked.connect(self.show_rules)
        self.button_check.clicked.connect(self.show_check)
        self.button_process.clicked.connect(self.show_matches)
        self.clear_check.clicked.connect(self.delete_check)
        self.clear_regex.clicked.connect(self.delete_matches)
        self.open_text.clicked.connect(self.text_open)
        self.clear_text.clicked.connect(self.delete_text)
        self.save_regex.clicked.connect(self.save_matches)

    def show_rules(self):
        self.rules = Rules()
        self.rules.show()

    def show_check(self):
        regex = self.input_regex.text()
        new_regex = []
        for item in regex:
            new_regex.append(item)
        for el in new_regex:
            if el == '\\' and len(new_regex) == 1:
                self.output_check.append(el + ' -> {}'.format(rules_dictionary.get(el)))
            elif el == '\\' and ord(new_regex[new_regex.index(el) + 1]) in range(65, 123):
                result = el + new_regex[new_regex.index(el) + 1]
                if result in rules_dictionary:
                    self.output_check.append(result + ' -> {}'.format(rules_dictionary.get(result)))
                    new_regex.remove(new_regex[new_regex.index(el) + 1])
            elif el not in rules_dictionary and new_regex[new_regex.index(el) - 1] != ("\\"):
                self.output_check.append(el + '-> {}'.format('just find all occurrences of this symbol in the text'))
            elif el in rules_dictionary:
                self.output_check.append(el + '-> {}'.format(rules_dictionary.get(el)))
            elif el == '[':
                el = '[]'
                self.output_check.append(el + ' -> {}'.format(rules_dictionary.get(el)))
            elif el == '{':
                el = '{}'
                self.output_check.append(el + ' -> {}'.format(rules_dictionary.get(el)))
            elif el == '(':
                el = '()'
                self.output_check.append(el + ' -> {}'.format(rules_dictionary.get(el)))

    def delete_check(self):
        self.output_check.clear()

    def text_open(self):
        filename = QFileDialog.getOpenFileName(self, 'Save file', os.getenv('HOME'))
        with open(filename[0], 'r') as f:
            file = f.read()
            self.input_text.setText(file)

    def delete_text(self):
        self.input_text.clear()

    def show_matches(self):
        regex = self.input_regex.text()
        text = self.input_text.toPlainText()
        matches = re.findall(regex, text)
        for word in matches:
            print(word)
            self.output_regex.append(str(word))
        self.output_regex.append('Total:{}'.format(len(matches)))

    def delete_matches(self):
        self.output_regex.clear()

    def save_matches(self):
        filename = QFileDialog.getSaveFileName(self, 'Save file', os.getenv('HOME'))
        with open(filename[0], 'w') as f:
            my_text = self.output_regex.toPlainText()
            f.write(my_text)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
