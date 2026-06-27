from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)

from dataBase import DataBase


STYLE = """
QWidget {
    background-color: #1e1e1e;
    color: #ffffff;
    font-size: 14px;
}

QLineEdit {
    padding: 8px;
    border: 1px solid #555;
    border-radius: 8px;
}

QPushButton {
    padding: 8px;
    border: none;
    border-radius: 8px;
    background-color: #3b82f6;
    color: #ffffff;
}

QPushButton:hover {
    background-color: #2563eb;
}

QTableWidget {
    background-color: #2d2d2d;
    gridline-color: #444;
}

QHeaderView::section {
    background-color: #333;
    color: #ffffff;
    padding: 5px;
}
"""


class BooksApp(QWidget):
    def __init__(self):
        super().__init__()

        self.db = DataBase()
        self.selected_book_id = None

        self.setWindowTitle("Книги")
        self.resize(760, 460)
        self.setStyleSheet(STYLE)

        self.init_ui()
        self.show_books()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Книги")
        title.setStyleSheet("font-size: 22px;")

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название")

        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Автор")

        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Год")

        form_layout = QHBoxLayout()
        form_layout.addWidget(self.title_input)
        form_layout.addWidget(self.author_input)
        form_layout.addWidget(self.year_input)

        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить")
        self.show_button = QPushButton("Показать")
        self.search_button = QPushButton("Найти")
        self.update_button = QPushButton("Изменить")
        self.delete_button = QPushButton("Удалить")
        self.clear_button = QPushButton("Очистить")

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.show_button)
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Автор", "Год"])
        self.table.cellClicked.connect(self.select_book)

        self.add_button.clicked.connect(self.add_book)
        self.show_button.clicked.connect(self.show_books)
        self.search_button.clicked.connect(self.search_book)
        self.update_button.clicked.connect(self.update_book)
        self.delete_button.clicked.connect(self.delete_book)
        self.clear_button.clicked.connect(self.clear_fields)

        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def get_form_data(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        year_text = self.year_input.text().strip()

        if not title or not author or not year_text:
            QMessageBox.warning(self, "Ошибка", "Заполните поля: Название, Автор, Год.")
            return None

        try:
            year = int(year_text)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Год должен быть числом.")
            return None

        return title, author, year

    def add_book(self):
        data = self.get_form_data()
        if data is None:
            return

        self.db.add_book(*data)
        self.clear_fields()
        self.show_books()
        QMessageBox.information(self, "Готово", "Книга добавлена.")

    def show_books(self):
        books = self.db.get_books()
        self.fill_table(books)

    def search_book(self):
        title = self.title_input.text().strip()

        if not title:
            QMessageBox.warning(self, "Ошибка", "Введите название книги для поиска.")
            return

        books = self.db.search_books(title)
        self.fill_table(books)

        if not books:
            QMessageBox.information(self, "Результат", "Книга не найдена.")

    def update_book(self):
        if self.selected_book_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите книгу в таблице.")
            return

        data = self.get_form_data()
        if data is None:
            return

        self.db.update_book(self.selected_book_id, *data)
        self.clear_fields()
        self.show_books()
        QMessageBox.information(self, "Готово", "Данные книги изменены.")

    def delete_book(self):
        if self.selected_book_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите книгу в таблице.")
            return

        self.db.delete_book(self.selected_book_id)
        self.clear_fields()
        self.show_books()
        QMessageBox.information(self, "Готово", "Книга удалена.")

    def fill_table(self, books):
        self.table.setRowCount(0)

        for row, book in enumerate(books):
            self.table.insertRow(row)
            for column, value in enumerate(book):
                self.table.setItem(row, column, QTableWidgetItem(str(value)))

    def select_book(self, row, column):
        self.selected_book_id = int(self.table.item(row, 0).text())
        self.title_input.setText(self.table.item(row, 1).text())
        self.author_input.setText(self.table.item(row, 2).text())
        self.year_input.setText(self.table.item(row, 3).text())

    def clear_fields(self):
        self.selected_book_id = None
        self.title_input.clear()
        self.author_input.clear()
        self.year_input.clear()
        self.table.clearSelection()
