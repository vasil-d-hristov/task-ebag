Download Repo

cd C:\Users\Vasil\Documents\Django\task\task-ebag
.\venv\Scripts\activate
pip install -r requirements.txt
cd ebag
[py manage.py makemigrations]
py manage.py migrate
py manage.py test
py manage.py reset_db -c 10 -s 10
py manage.py runserver