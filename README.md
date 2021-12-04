# UGTMS - Project for Dissertasion

### A Timesheet Management System.

> Universities often recruit several undergraduate and postgraduate students as lab assistants, tutors, or to assist with marking of student assignments or projects. Following recruitment, lab assistants and/or tutors will normally have to submit monthly timesheets with details of hours worked. These timesheets will have to be signed off by a suitable member of staff before they can receive payments. The purpose of this project is to research and develop a web application to automate these processes.

You can use the web application at: https://ugtms.herokuapp.com/

***Users credentials***
| username | password | role |
| -------- | -------- | -------- |
| admin    | admin    | administrator     |
| Martin   | Pokemon52 | Verifier |
| Ewa      | Pokemon52 | Payer |
| 042069d  | Pokemon52 | Student|


To run the project locally run the following commands.

```
brew install postgresql (on a Desktop for psycopg2)
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

To create an Admin user and his profile:

```
python manage.py createsuperuser
python manage.py shell
from django.contrib.auth.models import User
from members.models import UserProfile
userSelected = User.objects.get(pk=1)
userSelected, created = UserProfile.objects.get_or_create(user=userSelected)
```

then go to Admin Panel and add the User Roles available and you're ready to go.