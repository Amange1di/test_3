import sys

from PyQt6.QtWidgets import QApplication

from interface import BooksApp


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BooksApp()
    window.show()
    sys.exit(app.exec())


# Ответы на вопросы:
# 1. Что такое CRUD?
# CRUD - это четыре основные операции с данными:
# Create (создать), Read (прочитать), Update (изменить), Delete (удалить).
#
# 2. Что такое декомпозиция?
# Декомпозиция - это разделение большой задачи на небольшие понятные части.
#
# 3. Какая команда показывает текущую папку в Linux?
# Команда pwd.
#
# 4. Что такое localhost?
# localhost - это имя собственного компьютера в сети, обычно адрес 127.0.0.1.
