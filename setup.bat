@echo off
echo ============================================
echo  Setup - Masterclass Etudiant Entrepreneur
echo ============================================

echo.
echo [1/4] Creation de l'environnement virtuel...
python -m venv venv

echo.
echo [2/4] Activation et installation des packages...
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo.
echo [3/4] Migrations base de donnees...
python manage.py makemigrations
python manage.py migrate

echo.
echo [4/4] Creation du superuser admin...
python manage.py createsuperuser

echo.
echo ============================================
echo  Lancer le serveur : python manage.py runserver
echo  Admin :             http://127.0.0.1:8000/admin/
echo  Site :              http://127.0.0.1:8000/
echo ============================================
pause
