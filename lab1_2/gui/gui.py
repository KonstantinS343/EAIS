# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtWidgets

import re
import nltk
import os
import json
import logging
import time

from src.morphy_logic import filter_rows, morphy_logic_main
from src.text_corpora import main_corpus
from src.syntactic_analysis import main_analysis, filter_syntactic_rows, split_sentence
from conf.metadata import metadata
from gui.dialog import Ui_Dialog


logging.basicConfig(
    format="[%(asctime)s | %(levelname)s]: %(message)s",
    datefmt="%m.%d.%Y %H:%M:%S",
    level=logging.INFO,
)

HELP_TEXT = """Справка:
1. Для импорта текста необходимо нажать на кнопку "Импортировать текст", также есть возможность писать текст вручную.
2. Для разбора текста необходимо нажать кнопку "Разобрать текст", после чего появится таблица с результатом.

В данной таблице можно редактировать дополнительнею информацию, которая представлена в 3 колонке.

4. При нажатии на "Очистить", уберется таблица, при поыторном нажатии мы удалим весь введенный текст.
5. Также есть возможность сохранить текст в файл в формате JSON, для комфортной визуализации результатов.

6. Кроме того, после разбора текста можно начажать на "Фильрация и поиск" для фильтрации и поиска по словам, частоте и дополнительной информации.

Удачи!
"""


#  class Signals(QtCore.QObject):
#    item_inserted = QtCore.pyqtSignal()


class Ui_MainWindow(object):
    def __init__(self, mode: str, column: int):
        self.mode = mode
        self.column = column
        super().__init__()

    def setupUi(self, MainWindow):
        # self.signals = Signals()
        self._opened_files = []

        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(1000, 600)
        # MainWindow.setMinimumSize(QtCore.QSize(1000, 600))
        MainWindow.resize(1208, 600)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 0))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.clear_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_button.setMinimumSize(QtCore.QSize(194, 0))
        self.clear_button.setObjectName("clear_button")
        self.gridLayout.addWidget(self.clear_button, 6, 4, 1, 2)

        self.text_area = QtWidgets.QTextEdit(self.centralwidget)
        self.text_area.setObjectName("text_area")
        self.text_area.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.text_area.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )

        self.gridLayout.addWidget(self.text_area, 5, 0, 1, 2)

        self.analyze_text_button = QtWidgets.QPushButton(self.centralwidget)
        self.analyze_text_button.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed
        )
        self.analyze_text_button.setMinimumSize(QtCore.QSize(194, 0))
        self.analyze_text_button.setObjectName("analyze_text_button")
        self.gridLayout.addWidget(self.analyze_text_button, 6, 1, 1, 1)

        self.import_text_button = QtWidgets.QPushButton(self.centralwidget)
        self.import_text_button.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed
        )
        self.import_text_button.setMinimumSize(QtCore.QSize(194, 0))
        self.import_text_button.setObjectName("import_text_button")
        self.gridLayout.addWidget(self.import_text_button, 6, 0, 1, 1)

        self.result_table = QtWidgets.QTableWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.result_table.sizePolicy().hasHeightForWidth())
        self.result_table.setSizePolicy(sizePolicy)
        self.result_table.setObjectName("result_table")
        self.result_table.setColumnCount(0)
        self.result_table.setRowCount(0)

        self.result_table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.result_table.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.result_table.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.result_table.setAlternatingRowColors(False)
        self.result_table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems
        )
        self.result_table.setTextElideMode(QtCore.Qt.TextElideMode.ElideMiddle)
        self.result_table.setCornerButtonEnabled(False)
        self._set_result_table_vertical_headers()
        self.result_table.setEditTriggers(
            QtWidgets.QTableWidget.EditTrigger.NoEditTriggers
        )
        self.result_table.cellDoubleClicked.connect(self.on_cell_double_click)

        self.gridLayout.addWidget(self.result_table, 5, 2, 1, 4)

        self.search_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_button.setObjectName("search_button")
        self.gridLayout.addWidget(self.search_button, 0, 3, 1, 1)

        self.help_button = QtWidgets.QPushButton(self.centralwidget)
        self.help_button.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed
        )
        self.help_button.setObjectName("help_button")
        self.help_button.setCheckable(True)
        self.gridLayout.addWidget(self.help_button, 0, 0, 1, 1)

        if self.mode == '2':
            self.contex = QtWidgets.QPushButton(self.centralwidget)
            self.contex.setSizePolicy(
                QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed
            )
            self.contex.setObjectName("contex")
            self.gridLayout.addWidget(self.contex, 0, 1, 1, 1)

        # self.save_text_as_button = QtWidgets.QPushButton(self.centralwidget)
        # self.save_text_as_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
        # QtWidgets.QSizePolicy.Policy.Fixed)
        # self.save_text_as_button.setMinimumSize(QtCore.QSize(194, 0))
        # self.save_text_as_button.setObjectName("save_text_as_button")
        # self.gridLayout.addWidget(self.save_text_as_button, 3, 0, 1, 1)

        # self.save_text_button = QtWidgets.QPushButton(self.centralwidget)
        # self.save_text_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        # self.save_text_button.setMinimumSize(QtCore.QSize(194, 0))
        # self.save_text_button.setObjectName("save_text_button")
        # self.gridLayout.addWidget(self.save_text_button, 3, 1, 1, 1)

        self.search_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.search_line_edit.setObjectName("search_line_edit")
        self.gridLayout.addWidget(self.search_line_edit, 0, 4, 1, 2)

        self.save_anal = QtWidgets.QPushButton(self.centralwidget)
        self.save_anal.setMinimumSize(QtCore.QSize(194, 0))
        self.save_anal.setStyleSheet("Сохранить результат разбора в файл")
        self.save_anal.setObjectName("save_anal")
        self.gridLayout.addWidget(self.save_anal, 6, 2, 1, 2)

        self.help_area = QtWidgets.QTextBrowser(self.centralwidget)
        self.help_area.setObjectName("help_area")
        self.help_area.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        self.gridLayout.addWidget(self.help_area, 3, 0, 1, 6)

        self.max_frequency_spinbox = QtWidgets.QSpinBox(self.centralwidget)
        self.max_frequency_spinbox.setAccelerated(True)
        self.max_frequency_spinbox.setMaximum(2147483647)
        self.max_frequency_spinbox.setObjectName("max_frequency_spinbox")
        self.gridLayout.addWidget(self.max_frequency_spinbox, 0, 5, 1, 1)

        self.min_frequency_spinbox = QtWidgets.QSpinBox(self.centralwidget)
        self.min_frequency_spinbox.setAccelerated(True)
        self.min_frequency_spinbox.setMaximum(2147483647)
        self.min_frequency_spinbox.setStepType(
            QtWidgets.QAbstractSpinBox.DefaultStepType
        )
        self.min_frequency_spinbox.setObjectName("min_frequency_spinbox")
        self.gridLayout.addWidget(self.min_frequency_spinbox, 0, 4, 1, 1)

        self.part_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.part_line_edit.setClearButtonEnabled(True)
        self.part_line_edit.setObjectName("part_line_edit")
        self.gridLayout.addWidget(self.part_line_edit, 0, 4, 1, 2)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1208, 30))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menuBar)

        self.lexem_filtration_action = QtWidgets.QAction(MainWindow)
        self.lexem_filtration_action.setCheckable(True)
        self.lexem_filtration_action.setChecked(True)
        self.lexem_filtration_action.setObjectName("lexem_filtration_action")

        self.frequency_filtration_action = QtWidgets.QAction(MainWindow)
        self.frequency_filtration_action.setCheckable(True)
        self.frequency_filtration_action.setObjectName("frequency_filtration_action")
        self.part_filtration_action = QtWidgets.QAction(MainWindow)
        self.part_filtration_action.setCheckable(True)
        self.part_filtration_action.setObjectName("part_filtration_action")

        self.menu.addAction(self.lexem_filtration_action)
        self.menu.addSeparator()
        self.menu.addAction(self.frequency_filtration_action)
        self.menu.addSeparator()
        self.menu.addAction(self.part_filtration_action)
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self._connect_all(MainWindow)

        self.clear_button.setEnabled(False)
        self.clear_button.setVisible(False)
        self.analyze_text_button.setEnabled(False)
        self.result_table.setEnabled(False)
        self.result_table.setVisible(False)
        self.search_button.setEnabled(False)
        self.search_button.setVisible(False)
        # self.save_text_as_button.setEnabled(False)
        # self.save_text_button.setEnabled(False)
        self.search_line_edit.setEnabled(False)
        self.search_line_edit.setVisible(False)
        self.save_anal.setEnabled(False)
        self.save_anal.setVisible(False)
        self.help_area.setEnabled(False)
        self.help_area.setVisible(False)
        self.max_frequency_spinbox.setEnabled(False)
        self.max_frequency_spinbox.setVisible(False)
        self.min_frequency_spinbox.setEnabled(False)
        self.min_frequency_spinbox.setVisible(False)
        self.part_line_edit.setEnabled(False)
        self.part_line_edit.setVisible(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Анализатор"))
        self.save_anal.setToolTip(
            _translate("MainWindow", "Сохранить результаты анализа текста в файл")
        )
        self.save_anal.setText(_translate("MainWindow", "Сохранить разбор"))
        self.help_button.setToolTip(_translate("MainWindow", "Открыть систему помощи"))
        self.help_button.setText(_translate("MainWindow", "Помощь"))
        if self.mode == '2':
            self.contex.setToolTip(
                _translate("MainWindow", "Поиск контекста использования слова")
            )
            self.contex.setText(_translate("MainWindow", "Контекст"))
        self.analyze_text_button.setToolTip(
            _translate("MainWindow", "Запустить анализ текста")
        )
        self.analyze_text_button.setText(_translate("MainWindow", "Разобрать текст"))
        self.clear_button.setToolTip(
            _translate(
                "MainWindow",
                "Очистить таблицу (нажмите второй раз, чтобы скрыть таблицу)",
            )
        )
        self.clear_button.setText(_translate("MainWindow", "Очистить"))
        self.help_area.setText(_translate("MainWindow", HELP_TEXT))
        self.import_text_button.setToolTip(
            _translate("MainWindow", "Загрузить текст из файла")
        )
        self.import_text_button.setText(_translate("MainWindow", "Импортировать текст"))
        self.max_frequency_spinbox.setToolTip(
            _translate(
                "MainWindow",
                "Верхняя граница для фильтрации по частоте словоформы в тексте",
            )
        )
        self.max_frequency_spinbox.setSpecialValueText(
            _translate("MainWindow", "Верхняя граница")
        )
        self.search_line_edit.setToolTip(
            _translate(
                "MainWindow",
                "Введите слово, по которому будет произведен поиск среди лексем и словоформ",
            )
        )
        self.search_line_edit.setPlaceholderText(
            _translate("MainWindow", "Введите слово для поиска...")
        )
        self.search_button.setToolTip(
            _translate("MainWindow", "Поиск/фильтрация по введенному условию")
        )
        self.search_button.setText(_translate("MainWindow", "Поиск"))
        self.min_frequency_spinbox.setToolTip(
            _translate(
                "MainWindow",
                "Нижняя границу для фильтрации по частоте словоформы в тексте",
            )
        )
        self.min_frequency_spinbox.setSpecialValueText(
            _translate("MainWindow", "Нижняя граница")
        )
        self.part_line_edit.setToolTip(
            _translate(
                "MainWindow", "Введите название части речи, чтобы отфильтровать вывод"
            )
        )
        self.part_line_edit.setPlaceholderText(
            _translate("MainWindow", "Введите название части речи...")
        )
        if self.mode != '3':
            self.menu.setTitle(_translate("MainWindow", "Фильтрация и поиск"))
        self.lexem_filtration_action.setText(
            _translate("MainWindow", "Поиск по словам")
        )
        self.frequency_filtration_action.setText(
            _translate("MainWindow", "Фильтрация по частоте словоформы")
        )
        self.part_filtration_action.setText(
            _translate("MainWindow", "Фильтрация по части речи")
        )
        self.part_filtration_action.setToolTip(
            _translate("MainWindow", "Фильтрация по части речи")
        )

    def _set_result_table_vertical_headers(self):
        self.result_table.setColumnCount(self.column)
        for i in range(self.column):
            item = QtWidgets.QTableWidgetItem()
            self.result_table.setHorizontalHeaderItem(i, item)

    def _add_result_table_vertical_header(self):
        self.result_table.setRowCount(self.result_table.rowCount() + 1)
        item = QtWidgets.QTableWidgetItem()
        item.setText(str(self.result_table.rowCount()))
        self.result_table.setVerticalHeaderItem(self.result_table.rowCount() - 1, item)

    def emplace_word(self, word: str, amount_in_text: int, additional_info: str):
        self._add_result_table_vertical_header()
        word_item = QtWidgets.QTableWidgetItem()
        word_item.setText(word)
        row_to_insert = self.result_table.rowCount() - 1
        self.result_table.setItem(row_to_insert, 0, word_item)
        amount_in_text_item = QtWidgets.QTableWidgetItem()
        amount_in_text_item.setText(str(amount_in_text))
        self.result_table.setItem(row_to_insert, 1, amount_in_text_item)
        additional_info_item = QtWidgets.QTableWidgetItem()
        additional_info_item.setText(additional_info)
        self.result_table.setItem(row_to_insert, 2, additional_info_item)
        if not self.save_anal.isEnabled():
            self.save_anal.setEnabled(True)

    def emplace_word2(self, sentence: str):
        self._add_result_table_vertical_header()
        word_item = QtWidgets.QTableWidgetItem()
        word_item.setText(sentence)
        row_to_insert = self.result_table.rowCount() - 1
        self.result_table.setItem(row_to_insert, 0, word_item)
        if not self.save_anal.isEnabled():
            self.save_anal.setEnabled(True)

    def on_cell_double_click(self, row, column):
        item = self.result_table.item(row, column)
        sentence = item.text()
        main_analysis(sentence)

    def _connect_all(self, MainWindow):
        self.text_area.textChanged.connect(self._text_area_edited)
        self.import_text_button.clicked.connect(
            lambda: self._import_filename(MainWindow)
        )
        self.analyze_text_button.clicked.connect(self.analyze_text_button_clicked)
        self.clear_button.clicked.connect(self._clear_button_clicked)
        self.help_button.clicked.connect(self.help_button_clicked)
        if self.mode == '2':
            self.contex.clicked.connect(lambda: self.contex_button_clicked(MainWindow))
        self.search_line_edit.textChanged.connect(self._search_line_text_changed)
        self.search_button.clicked.connect(self._search_button_clicked)
        self.save_anal.clicked.connect(lambda: self._save_anal_button_clicked(MainWindow))
        self.part_line_edit.textChanged.connect(self._part_line_text_changed)
        self.min_frequency_spinbox.valueChanged.connect(
            self._min_freq_spinbox_value_changed
        )
        self.max_frequency_spinbox.valueChanged.connect(
            self._max_freq_spinbox_value_changed
        )

        self.lexem_filtration_action.triggered.connect(
            self._lexem_filtration_action_triggered
        )
        self.frequency_filtration_action.triggered.connect(
            self._frequency_filtration_action_triggered
        )
        self.part_filtration_action.triggered.connect(
            self._part_filtration_action_triggered
        )

    def _text_area_edited(self):
        if not re.sub(r"\s+", "", self.text_area.toPlainText()):
            self.analyze_text_button.setEnabled(False)
            # self.save_text_button.setEnabled(False)
            # self.save_text_as_button.setEnabled(False)
        elif not self.analyze_text_button.isEnabled():
            self.analyze_text_button.setEnabled(True)
            # self.save_text_button.setEnabled(True)
            # self.save_text_as_button.setEnabled(True)

    def _import_filename(self, MainWindow):
        filename, ok = QtWidgets.QFileDialog.getOpenFileName(
            MainWindow,
            "импортировать файл с текстом",
            "/home",
            "Text files (*.txt *.rtf)",
        )
        if filename:
            self._opened_files.append(filename)
            if re.sub(r"\s+", "", self.text_area.toPlainText()):
                question = QtWidgets.QMessageBox.question(
                    MainWindow,
                    "Подтверждение действия",
                    "Вы хотите расширить текущий текст содежимым выбранного файла? Если нет,\
                        то текущее содержимое поля с текстом очистится.",
                    QtWidgets.QMessageBox.StandardButton.Yes
                    | QtWidgets.QMessageBox.StandardButton.No,
                )
                with open(filename, "r") as fin:
                    if question == QtWidgets.QMessageBox.StandardButton.Yes:
                        self.text_area.insertPlainText(fin.read())
                        return
            with open(filename, "r") as fin:
                self.text_area.setText(fin.read())

    def _search_type(self):
        if self.lexem_filtration_action.isChecked():
            self.search_button.setVisible(True)
            self.search_line_edit.setVisible(True)
            self.search_line_edit.setEnabled(True)
        elif self.frequency_filtration_action.isChecked():
            self.search_button.setVisible(True)
            self.min_frequency_spinbox.setVisible(True)
            self.min_frequency_spinbox.setEnabled(True)
            self.max_frequency_spinbox.setVisible(True)
            self.max_frequency_spinbox.setEnabled(True)
        elif self.part_filtration_action.isChecked():
            self.search_button.setVisible(True)
            self.part_line_edit.setVisible(True)
            self.part_line_edit.setEnabled(True)

    def analyze_text_button_clicked(self):
        if not self.result_table.isEnabled():
            self.result_table.setVisible(True)
            self.clear_button.setVisible(True)
            self.result_table.setEnabled(True)
            self.clear_button.setEnabled(True)
            self._search_type()
            self.save_anal.setVisible(True)
        elif not self.result_table.rowCount() == 0:
            self._clear_result_table()
        start = time.time()
        if self.mode == '2':
            self.result = main_corpus(self.text_area.toPlainText())
        elif self.mode == '1':
            self.result = morphy_logic_main(self.text_area.toPlainText())
        else:
            self.result = split_sentence(self.text_area.toPlainText())
            for sentence in self.result:
                self.emplace_word2(sentence)
            return
        logging.info(time.time() - start)
        for key, value in self.result.items():
            self.emplace_word(key, value["frequency"], value["additional information"])

    def _clear_result_table(self):
        self.save_anal.setEnabled(False)
        self.search_line_edit.clear()
        self.part_line_edit.clear()
        self.max_frequency_spinbox.clear()
        self.min_frequency_spinbox.clear()
        i = 0
        while i < self.result_table.rowCount():
            self.result_table.removeRow(0)

    def _clear_button_clicked(self):
        if self.result_table.rowCount() == 0:
            self.result_table.setEnabled(False)
            self.clear_button.setEnabled(False)
            self.result_table.setVisible(False)
            self.clear_button.setVisible(False)
            self.search_button.setEnabled(False)
            self.search_button.setVisible(False)
            self.search_line_edit.setVisible(False)
            self.search_line_edit.setEnabled(False)
            self.min_frequency_spinbox.setVisible(False)
            self.min_frequency_spinbox.setEnabled(False)
            self.max_frequency_spinbox.setVisible(False)
            self.max_frequency_spinbox.setEnabled(False)
            self.part_line_edit.setVisible(False)
            self.part_line_edit.setEnabled(False)
            self.save_anal.setEnabled(False)
            self.save_anal.setVisible(False)
        else:
            self._clear_result_table()

    def help_button_clicked(self):
        if self.help_button.isChecked():
            self.open_help_area()
        else:
            self.close_help_area()

    def contex_button_clicked(self, MainWindow):
        Dialog = QtWidgets.QDialog(parent=MainWindow)
        ui = Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()

    def open_help_area(self):
        self.clear_button.setEnabled(False)
        self.clear_button.setVisible(False)
        self.analyze_text_button.setEnabled(False)
        self.analyze_text_button.setVisible(False)
        self.result_table.setEnabled(False)
        self.result_table.setVisible(False)
        self.search_button.setEnabled(False)
        self.search_button.setVisible(False)
        self.search_line_edit.setVisible(False)
        self.search_line_edit.setEnabled(False)
        self.min_frequency_spinbox.setVisible(False)
        self.min_frequency_spinbox.setEnabled(False)
        self.max_frequency_spinbox.setVisible(False)
        self.max_frequency_spinbox.setEnabled(False)
        self.part_line_edit.setVisible(False)
        self.part_line_edit.setEnabled(False)
        self.save_anal.setEnabled(False)
        self.save_anal.setVisible(False)
        self.text_area.setEnabled(False)
        self.text_area.setVisible(False)
        self.import_text_button.setEnabled(False)
        self.import_text_button.setVisible(False)

        self.help_area.setEnabled(True)
        self.help_area.setVisible(True)

    def close_help_area(self):
        self.help_area.setEnabled(False)
        self.help_area.setVisible(False)

        self.text_area.setEnabled(True)
        self.text_area.setVisible(True)
        self.import_text_button.setEnabled(True)
        self.import_text_button.setVisible(True)
        self.analyze_text_button.setVisible(True)
        self._text_area_edited()

        if self.result_table.rowCount() > 0:
            self.save_anal.setEnabled(True)
            self.save_anal.setVisible(True)
            self.clear_button.setEnabled(True)
            self.clear_button.setVisible(True)
            self.result_table.setEnabled(True)
            self.result_table.setVisible(True)
            self._search_type()
        self._search_line_text_changed()

    def _search_line_text_changed(self):
        if self.lexem_filtration_action.isChecked():
            if not self.search_line_edit.text().replace(" ", ""):
                self.search_button.setEnabled(False)
            elif not self.search_button.isEnabled():
                self.search_button.setEnabled(True)

    def _min_freq_spinbox_value_changed(self):
        if self.frequency_filtration_action.isChecked():
            if self.max_frequency_spinbox.value() < self.min_frequency_spinbox.value():
                self.max_frequency_spinbox.setValue(self.min_frequency_spinbox.value())
            if (
                self.min_frequency_spinbox.value() == 0
                and self.max_frequency_spinbox.value() == 0
            ):
                self.search_button.setEnabled(False)
            elif not self.search_button.isEnabled():
                self.search_button.setEnabled(True)

    def _max_freq_spinbox_value_changed(self):
        if self.frequency_filtration_action.isChecked():
            if self.min_frequency_spinbox.value() > self.max_frequency_spinbox.value():
                self.min_frequency_spinbox.setValue(self.max_frequency_spinbox.value())
            if (
                self.max_frequency_spinbox.value() == 0
                and self.min_frequency_spinbox.value() == 0
            ):
                self.search_button.setEnabled(False)
            elif not self.search_button.isEnabled():
                self.search_button.setEnabled(True)

    def _part_line_text_changed(self):
        if self.part_filtration_action.isChecked():
            if not self.part_line_edit.text().replace(" ", ""):
                self.search_button.setEnabled(False)
            elif not self.search_button.isEnabled():
                self.search_button.setEnabled(True)

    def _search_button_clicked(self):
        flag = "word"
        if self.lexem_filtration_action.isChecked():
            word_to_search = self.search_line_edit.text().strip(" ")
            if self.mode == '3':
                words = filter_syntactic_rows(search_type=word_to_search, data=self.result)
            else:
                words = filter_rows(flag=flag, search_type=word_to_search, data=self.result)
            # Слово, по которому поиск будет
        elif self.frequency_filtration_action.isChecked():
            flag = "frequency"
            min_frequency = self.min_frequency_spinbox.value()
            max_frequency = self.max_frequency_spinbox.value()
            words = filter_rows(
                flag=flag, frequency=(min_frequency, max_frequency), data=self.result
            )
            # Слово, по которому поиск будет
        else:
            flag = "extra information"
            part_of_text_to_search = self.part_line_edit.text().strip(" ")
            words = filter_rows(
                flag=flag, search_type=part_of_text_to_search, data=self.result
            )
            # Часть речи, по которому поиск будет
        self._clear_result_table()
        if self.mode == '3':
            for sentence in words:
                self.emplace_word2(sentence)
        else:
            for key, value in words.items():
                self.emplace_word(
                    key, value["frequency"], metadata[nltk.pos_tag([key])[0][1]]
                )

    def _save_anal_button_clicked(self, MainWindow):
        filename, ok = QtWidgets.QFileDialog.getSaveFileName(
            MainWindow, "сохранить разбор как...", os.path.curdir, "Text files(*.json)"
        )
        if filename:
            with open(filename + ".json", "w") as fout:
                json.dump(self.result, fout, indent=4, ensure_ascii=False)
        pass

    def _lexem_filtration_action_triggered(self):
        if self.lexem_filtration_action.isChecked():
            if self.frequency_filtration_action.isChecked():
                self.frequency_filtration_action.setChecked(False)
                self.min_frequency_spinbox.setEnabled(False)
                self.min_frequency_spinbox.setVisible(False)
                self.max_frequency_spinbox.setEnabled(False)
                self.max_frequency_spinbox.setVisible(False)
            elif self.part_filtration_action.isChecked():
                self.part_filtration_action.setChecked(False)
                self.part_line_edit.setEnabled(False)
                self.part_line_edit.setVisible(False)
            if self.result_table.rowCount() > 0:
                self.search_line_edit.setVisible(True)
                self.search_line_edit.setEnabled(True)
                if not self.search_button.isVisible():
                    self.search_button.setVisible(True)
        else:
            self.search_button.setEnabled(False)
            self.search_button.setVisible(False)
            self.search_line_edit.setEnabled(False)
            self.search_line_edit.setVisible(False)

    def _frequency_filtration_action_triggered(self):
        if self.frequency_filtration_action.isChecked():
            if self.lexem_filtration_action.isChecked():
                self.lexem_filtration_action.setChecked(False)
                self.search_line_edit.setEnabled(False)
                self.search_line_edit.setVisible(False)
            elif self.part_filtration_action.isChecked():
                self.part_filtration_action.setChecked(False)
                self.part_line_edit.setEnabled(False)
                self.part_line_edit.setVisible(False)
            if self.result_table.rowCount() > 0:
                self.min_frequency_spinbox.setVisible(True)
                self.min_frequency_spinbox.setEnabled(True)
                self.max_frequency_spinbox.setVisible(True)
                self.max_frequency_spinbox.setEnabled(True)
                if not self.search_button.isVisible():
                    self.search_button.setVisible(True)
        else:
            self.search_button.setEnabled(False)
            self.search_button.setVisible(False)
            self.min_frequency_spinbox.setEnabled(False)
            self.min_frequency_spinbox.setVisible(False)
            self.max_frequency_spinbox.setEnabled(False)
            self.max_frequency_spinbox.setVisible(False)

    def _part_filtration_action_triggered(self):
        if self.part_filtration_action.isChecked():
            if self.lexem_filtration_action.isChecked():
                self.lexem_filtration_action.setChecked(False)
                self.search_line_edit.setEnabled(False)
                self.search_line_edit.setVisible(False)
            elif self.frequency_filtration_action.isChecked():
                self.frequency_filtration_action.setChecked(False)
                self.min_frequency_spinbox.setEnabled(False)
                self.min_frequency_spinbox.setVisible(False)
                self.max_frequency_spinbox.setEnabled(False)
                self.max_frequency_spinbox.setVisible(False)
            if self.result_table.rowCount() > 0:
                self.part_line_edit.setVisible(True)
                self.part_line_edit.setEnabled(True)
                if not self.search_button.isVisible():
                    self.search_button.setVisible(True)
        else:
            self.search_button.setEnabled(False)
            self.search_button.setVisible(False)
            self.part_line_edit.setEnabled(False)
            self.part_line_edit.setVisible(False)
