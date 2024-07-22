import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QTableWidget, QTableWidgetItem, QComboBox, QHeaderView, QCheckBox
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from data.items_data_weapon import *
from data.items_data_equipment import *
from data.items import *
from api_albion import *
from data._resources import *
import json
import io
import pandas as pd

class EmittingStream(QObject):
    text_written = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.buffer = io.StringIO()

    def write(self, text):
        self.buffer.write(text)
        self.text_written.emit(text)

    def flush(self):
        self.buffer.flush()

class ProcessThread(QThread):
    def __init__(self, update_output_callback, enable_view_table_button_callback, check_sell_zero, check_buy_zero):
        super().__init__()
        self.update_output_callback = update_output_callback
        self.enable_view_table_button_callback = enable_view_table_button_callback
        self.check_sell_zero = check_sell_zero
        self.check_buy_zero = check_buy_zero

    def run(self):
        process(self.update_output_callback, self.enable_view_table_button_callback, self.check_sell_zero, self.check_buy_zero)

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('MathiDDev Report')
        self.setWindowIcon(QIcon('data\\resources\\OffHand\\Shield\\T3_OFF_SHIELD.png'))
        self.setFixedSize(300, 200)

        font = QFont('Arial', 10)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QLineEdit {
                padding: 5px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 5px;
                color: black;
            }
            QPushButton {
                background-color: #5cb85c;
                color: white;
                font-size: 14px;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #4cae4c;
            }
        """)

        main_layout = QVBoxLayout()

        title_label = QLabel('WELCOME')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #5cb85c;")
        main_layout.addWidget(title_label)

        form_layout = QVBoxLayout()

        username_layout = QHBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Username')
        username_layout.addWidget(self.username_input)
        form_layout.addLayout(username_layout)

        password_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(self.password_input)
        form_layout.addLayout(password_layout)

        main_layout.addLayout(form_layout)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login)
        main_layout.addWidget(self.login_button)

        self.setLayout(main_layout)
        self.center()

    def center(self):
        screen = self.screen().geometry()
        size = self.geometry()
        self.move(
            int((screen.width() - size.width()) / 2),
            int((screen.height() - size.height()) / 2)
        )

    def login(self):
        self.statusLogin = False
        username = self.username_input.text()
        password = self.password_input.text()

        if True:  # Authentication test
            self.statusLogin = True

        if self.statusLogin:
            print('LOGIN TEST')
            self.open_main_window()

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Batch Executor')
        self.setFixedSize(1000, 600)
        self.setWindowIcon(QIcon('data\\resources\\OffHand\\Shield\\T3_OFF_SHIELD.png'))

        self.check_sell_zero = False
        self.check_buy_zero = False

        main_layout = QVBoxLayout()

        title_label = QLabel('Batch Executor')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #333;")
        main_layout.addWidget(title_label)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        main_layout.addWidget(self.text_edit)

        buttons_layout = QHBoxLayout()

        self.execute_button = QPushButton('Execute Batch')
        self.execute_button.setFont(QFont('Arial', 14))
        self.execute_button.clicked.connect(self.execute_batch)
        buttons_layout.addWidget(self.execute_button)

        self.view_table_button = QPushButton('Ver Tabla')
        self.view_table_button.setFont(QFont('Arial', 14))
        self.view_table_button.setStyleSheet("background-color: red; color: white;")
        self.view_table_button.setEnabled(False)
        self.view_table_button.clicked.connect(self.view_table)
        buttons_layout.addWidget(self.view_table_button)

        main_layout.addLayout(buttons_layout)

        checkboxes_layout = QHBoxLayout()
        self.sell_zero_checkbox = QCheckBox('Filter Sell Zero')
        self.sell_zero_checkbox.stateChanged.connect(self.toggle_sell_zero)
        checkboxes_layout.addWidget(self.sell_zero_checkbox)

        self.buy_zero_checkbox = QCheckBox('Filter Buy Zero')
        self.buy_zero_checkbox.stateChanged.connect(self.toggle_buy_zero)
        checkboxes_layout.addWidget(self.buy_zero_checkbox)

        main_layout.addLayout(checkboxes_layout)

        self.setLayout(main_layout)
        self.center()

        self.output_stream = EmittingStream()
        self.output_stream.text_written.connect(self.update_output)
        sys.stdout = self.output_stream

    def center(self):
        screen = self.screen().geometry()
        size = self.geometry()
        self.move(
            int((screen.width() - size.width()) / 2),
            int((screen.height() - size.height()) / 2)
        )

    def execute_batch(self):
        self.execute_button.setEnabled(False)
        self.view_table_button.setEnabled(False)
        self.view_table_button.setStyleSheet("background-color: red; color: white;")
        self.thread = ProcessThread(self.update_output, self.enable_view_table_button, self.check_sell_zero, self.check_buy_zero)
        self.thread.start()

    def update_output(self, output):
        self.text_edit.append(output)
        self.text_edit.ensureCursorVisible()

    def enable_view_table_button(self):
        self.view_table_button.setEnabled(True)
        self.view_table_button.setStyleSheet("background-color: green; color: white;")
        self.execute_button.setEnabled(True)

    def view_table(self):
        self.table_window = ViewTable()
        self.table_window.show()

    def toggle_sell_zero(self, state):
        self.check_sell_zero = not self.check_sell_zero

    def toggle_buy_zero(self, state):
        self.check_buy_zero = not self.check_buy_zero

class ViewTable(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('View Table')
        self.setFixedSize(950, 600)
        self.setWindowIcon(QIcon('data\\resources\\OffHand\\Shield\\T3_OFF_SHIELD.png'))

        main_layout = QVBoxLayout()

        # Filtro
        filter_layout = QHBoxLayout()
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText('Search by Name_ES or Name_EN')
        self.filter_input.textChanged.connect(self.filter_table)
        filter_layout.addWidget(self.filter_input)
        main_layout.addLayout(filter_layout)

        # ComboBox
        self.sheet_selector = QComboBox()
        self.sheet_selector.currentIndexChanged.connect(self.load_data)
        filter_layout.addWidget(self.sheet_selector)

        self.table = QTableWidget()
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)
        self.center()

        self.load_sheets()

    def center(self):
        screen = self.screen().geometry()
        size = self.geometry()
        self.move(
            int((screen.width() - size.width()) / 2),
            int((screen.height() - size.height()) / 2)
        )

    def load_sheets(self):
        file_path = '_item_prices.xlsx'
        self.excel_data = pd.ExcelFile(file_path)
        self.sheet_selector.addItems(self.excel_data.sheet_names)
        self.load_data()

    def load_data(self):
        sheet_name = self.sheet_selector.currentText()
        if not sheet_name:
            return

        df = pd.read_excel(self.excel_data, sheet_name=sheet_name)

        if df.empty:
            return

        self.df = df 
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for row in df.itertuples():
            for col, value in enumerate(row[1:]):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row.Index, col, item)

    def filter_table(self):
        filter_text = self.filter_input.text().lower()
        for row in range(self.table.rowCount()):
            item_es = self.table.item(row, self.df.columns.get_loc('Name ES'))
            item_en = self.table.item(row, self.df.columns.get_loc('Name EN'))
            if item_es and item_en:
                item_text_es = item_es.text().lower()
                item_text_en = item_en.text().lower()
                self.table.setRowHidden(row, filter_text not in item_text_es and filter_text not in item_text_en)

def process(update_output_callback, enable_view_table_button_callback, check_sell_zero, check_buy_zero):
    Black_Market = 'Black Market'
    Caerleon_Market = '3005'
    Thetford_Market = '0007'
    Fort_Sterling_Market = '4002'
    Lymhurst_Market = '1002'
    Martlock_Market = '3008'
    Bridgewatch_Market = '2004'
    Brecilien_Market = '5003'
    request_location = f'{Black_Market},{Caerleon_Market},{Thetford_Market},{Fort_Sterling_Market},{Lymhurst_Market},{Martlock_Market},{Bridgewatch_Market},{Brecilien_Market}'

    print_and_flush('Item descriptions: Loading.', update_output_callback)
    ITEMS_ALL_DESCRIPTION = cargar_items_desde_archivo_items()
    print_and_flush('Item descriptions: Loaded.', update_output_callback)

    print_and_flush('Getting IDs.', update_output_callback)
    ids = obtener_resources_id()
    ids_unicos = obtener_resources_id_unicos()
    print_and_flush('Getting IDs completed.', update_output_callback)

    # REQUEST
    request = ''
    response = []
    contador = 0
    len_querys = 300
    print_and_flush('Building queries...', update_output_callback)

    for id in ids:
        contador += 1
        request += f'{id},'
        if contador == len_querys:
            res = get_item_prices(request, request_location)
            message = f'Query executed for {len_querys} items: {len(res)} results obtained.'
            print_and_flush(message, update_output_callback)
            response.extend(res)
            contador = 0
            request = ''

    # Residual IDs
    if request:
        res2 = get_item_prices(request, request_location)
        message = f'Query executed for {contador} items: {len(res2)} results obtained.'
        print_and_flush(message, update_output_callback)
        response.extend(res2)

    print_and_flush('Getting additional information.', update_output_callback)
    file_path = '_item_prices.xlsx'
    data_list = None
    with open('data/items.json', 'r', encoding='utf-8') as file:
        data_list = json.load(file)
    print_and_flush('Getting additional information completed.', update_output_callback)

    print_and_flush('Merging everything...', update_output_callback)
    items = merge_additional_info(response, data_list)
    
    if check_sell_zero:
        print_and_flush('Filter sell in zero...', update_output_callback)
        items = [item for item in items if item.sell_price_min != 0] 

    if check_buy_zero:
        print_and_flush('Filter buy in zero...', update_output_callback)
        items = [item for item in items if item.buy_price_max != 0] 

    # EXCEL
    print_and_flush('Saving information to Excel file...', update_output_callback)
    guardar_en_excel(items, file_path)
    print_and_flush(f'Data saved in {file_path}', update_output_callback)
    print_and_flush('Process status: ALL GOOD, I am a genius.', update_output_callback)
    
    enable_view_table_button_callback()

def print_and_flush(message, update_output_callback):
    print(message)
    sys.stdout.flush()
    update_output_callback(message)

def print_and_flush(message, update_output_callback):
    print(message)
    sys.stdout.flush()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_form = LoginForm()
    login_form.show()
    sys.exit(app.exec())
