#!/bin/bash

# Прерывать выполнение скрипта при ошибках
#set -e

# 1. Git pull для обновления репозитория
REPO_DIR="." # Corrected path

echo "Переход в директорию репозитория и обновление..."

cd "$REPO_DIR" || { echo "Ошибка: Не удалось перейти в директорию $REPO_DIR"; exit 1; }

git pull origin main || { echo "Ошибка: Не удалось выполнить git pull"; exit 1; }

# 2. Запуск тестов
TEST_FILE="test.py"

echo "Запуск тестов..."

if [ ! -f "$TEST_FILE" ]; then
    echo "Ошибка: Файл $TEST_FILE не найден."
    exit 1
fi

python3 "$TEST_FILE" || { echo "Ошибка: Тесты завершились с ошибкой"; exit 1; }


# 3. Проверка и создание package.spec
SPEC_FILE="package.spec"

echo "Проверка наличия $SPEC_FILE..."

if [ ! -f "$SPEC_FILE" ]; then
    echo "Файл $SPEC_FILE не найден. Создаём..."
    cat <<EOL > $SPEC_FILE
Name:           calc
Version:        1.0
Release:        1%{?dist}
Summary:        Example calculator application
License:        MIT
Source0:        project.tar.gz

%description
A simple calculator application.

%prep
%setup -q

%build
# Если требуется компиляция или сборка, добавьте команды здесь

%install
mkdir -p %{buildroot}/usr/local/bin
cp -r * %{buildroot}/usr/local/bin

%files
/usr/local/bin/*

%changelog
* $(date "+%a %b %d %Y") asfqx <[polinabrunina25@gmail.com](https://polinabrunina25@gmail.com)> - 1.0-1
- Initial RPM build

EOL
fi

# 4. Сборка RPM
echo "Сборка RPM пакета..."
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
cp "$SPEC_FILE" ~/rpmbuild/SPECS/
tar -czf ~/rpmbuild/SOURCES/project.tar.gz -C "/home/brunina_po/Desktop/calc" . || { echo "Ошибка: Не удалось создать архив"; exit 1; }
rpmbuild -ba ~/rpmbuild/SPECS/$(basename $SPEC_FILE) || { echo "Ошибка: Не удалось собрать RPM пакет"; exit 1; }

# 5. Установка RPM
RPM_FILE=$(find ~/rpmbuild/RPMS -name "*.rpm" | head -n 1)

if [ -z "$RPM_FILE" ]; then
    echo "Ошибка: RPM файл не найден."
    exit 1
fi

echo "Установка RPM пакета..."

sudo rpm -Uvh --force "$RPM_FILE" || { echo "Ошибка: Не удалось установить RPM пакет"; exit 1; }

# 6. Проверка и запуск программы
MAIN_SCRIPT="/usr/local/bin/main.py"

if [ ! -f "$MAIN_SCRIPT" ]; then
    echo "Ошибка: Главный файл $MAIN_SCRIPT не найден. Убедитесь, что он установлен."
    exit 1
fi

sudo chmod +x "$MAIN_SCRIPT"

echo "Запуск программы..."

$MAIN_SCRIPT || python3 "$MAIN_SCRIPT" || { echo "Ошибка: Не удалось запустить программу"; exit 1; }

echo "Готово!"
