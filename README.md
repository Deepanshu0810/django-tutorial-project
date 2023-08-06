# What is DJANGO
- python framework
- server side framework
- MVC(Model View Controller) framework
- MVT(Model View Template) framework
- easy to built API using django rest framework

# MVT
- Model: Database
- View: Business Logic
- Template: UI

# Setting up the environment
```bash
conda create -p env python
conda activate env/
pip install django
```

# Creating a project
```bash
django-admin startproject studybud
cd studybud
python manage.py runserver
```

# Creating an app
```bash
python manage.py startapp base
```

# Creating a superuser
```bash
python manage.py createsuperuser
```

# migrating the models
```bash
python manage.py makemigrations
python manage.py migrate
```

# StudyBud App

<img>![StudyBud](./Screenshots/home%20page.png)</img>
<img>![StudyBud](./Screenshots/login%20page.png)</img>
<img>![StudyBud](./Screenshots/user%20profile.png)</img>
<img>![StudyBud](./Screenshots/study%20room.png)</img>
