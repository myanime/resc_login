cd json
./import.sh
cd ..
cd web_app
python manage.py runserver 0.0.0.0:8000
xdg-open http://localhost:8000/modify_database