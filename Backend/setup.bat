@echo off
echo Configurando ambiente Django REST Framework...

REM Criar ambiente virtual
echo Criando ambiente virtual...
python -m venv venv

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instalar dependências
echo Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

REM Criar projeto Django
echo Criando projeto Django...
django-admin startproject config .

REM Criar app principal
echo Criando app principal...
python manage.py startapp apps

echo Setup concluido! Execute 'venv\Scripts\activate.bat' para ativar o ambiente virtual.
pause
