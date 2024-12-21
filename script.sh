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
"""
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

Requires: /bin/bash

%description
A simple calculator application.

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}/usr/local/bin
cp -r * %{buildroot}/usr/local/bin

%files
/usr/local/bin/*

%changelog
* $(date "+%a %b %d %Y") YourName <your@email.com> - 1.0-1
- Initial RPM build

EOL
fi

# 4. Сборка RPM
echo "Сборка RPM пакета..."
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
cd /home/brunina_po/Desktop/calc
mkdir calc-1.0
cp -r * calc-1.0
tar -czf ~/rpmbuild/SOURCES/project.tar.gz calc-1.0
rpmbuild -ba ~/rpmbuild/SPECS/package.spec || { echo "Ошибка: Не удалось собрать RPM пакет"; exit 1; }
cp "$SPEC_FILE" ~/rpmbuild/SPECS/

# 5. Установка RPM
RPM_FILE=$(find ~/rpmbuild/RPMS -name "*.rpm" | head -n 1)

if [ -z "$RPM_FILE" ]; then
    echo "Ошибка: RPM файл не найден."
    exit 1
fi

echo "Установка RPM пакета..."
ALIEN_OUTPUT=$(alien -t "$RPM_FILE")
sudo dpkg -i "$ALIEN_OUTPUT"
"""
# 3. Создание deb пакета (используя dh-make)
PACKAGE_NAME="calc" # Замените на имя вашего пакета
PACKAGE_VERSION="1.0"       # Замените на версию вашего пакета

echo "Создание deb пакета..."

# dh-make создает базовый шаблон. Вам нужно будет настроить файлы в созданной директории
dh-make --create --name="$PACKAGE_NAME" --copyright "MIT"

# Переходим в созданную директорию
cd "$PACKAGE_NAME" || { echo "Ошибка: Не удалось перейти в директорию $PACKAGE_NAME"; exit 1; }

# Необходимо настроить файлы в этой директории (например, debian/control, файлы в директории usr/local/bin и т.д.)
# Это включает в себя заполнение информации в debian/control,  копирование исполняемых файлов и т.д.

# После настройки, выполните сборку:
dpkg-buildpackage -us -uc || { echo "Ошибка: Не удалось собрать deb пакет"; exit 1; }


# 4. Установка deb пакета
DEB_FILE=$(find . -name "*.deb" | head -n 1)
if [ -z "$DEB_FILE" ]; then
    echo "Ошибка: DEB файл не найден."
    exit 1
fi
echo "Установка DEB пакета..."
sudo dpkg -i "$DEB_FILE" || { echo "Ошибка: Не удалось установить DEB пакет"; exit 1; }
# 6. Проверка и запуск программы
MAIN_SCRIPT="/home/brunina_po/Desktop/calc/main.py"

if [ ! -f "$MAIN_SCRIPT" ]; then
    echo "Ошибка: Главный файл $MAIN_SCRIPT не найден. Убедитесь, что он установлен."
    exit 1
fi

sudo chmod +x "$MAIN_SCRIPT"

echo "Запуск программы..."

$MAIN_SCRIPT || python3 "$MAIN_SCRIPT" || { echo "Ошибка: Не удалось запустить программу"; exit 1; }

echo "Готово!"
