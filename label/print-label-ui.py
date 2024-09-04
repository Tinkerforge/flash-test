#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import json
import traceback
from datetime import datetime

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system('python3 ../src/pyuic5-fixed.py -o ui_print_label_ui.py print-label-ui.ui')

from ui_print_label_ui import Ui_PrintLabelUI

class PrintLabelUI(QMainWindow, Ui_PrintLabelUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.button_print_label.clicked.connect(self.print_label)

        with open('print-label-ui-products.json', 'r') as f:
            for name, sku in sorted(json.loads(f.read())):
                self.combo_product.addItem('{0} [{1}]'.format(name, sku), (name, sku))

        self.combo_product.insertSeparator(self.combo_product.count())
        self.combo_product.addItem('Manuell')

        self.combo_product.currentIndexChanged.connect(lambda *args: self.update_ui_state())

        self.update_ui_state()

    def update_ui_state(self):
        data = self.combo_product.currentData()

        self.label_name.setVisible(data == None)
        self.edit_name.setVisible(data == None)
        self.label_sku.setVisible(data == None)
        self.edit_sku.setVisible(data == None)

    def print_label(self):
        try:
            data = self.combo_product.currentData()

            if data != None:
                name, sku = data
            else:
                name = self.edit_name.text()
                sku = self.edit_sku.text()

            subprocess.check_call([
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 'print-label.py'),
                '-c', str(self.spin_copies.value()),
                '-t', self.combo_type.currentText().lower(),
                name,
                sku,
                datetime.now().strftime('%Y-%m-%d'),
                '-',
                '-'
            ])
        except:
            traceback.print_exc()
            QMessageBox.critical(self, 'Druckproblem', 'Konnte Etikett nicht drucken:\nTraceback ist im Terminal')

def main():
    app = QApplication([])
    app.setWindowIcon(QIcon('logo.png'))

    window = PrintLabelUI()

    window.show()

    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())
