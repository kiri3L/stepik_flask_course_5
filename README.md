# stepik_flask_course_5

Перед первым запуском необходимо выполнить следующие действия


1. Создать переменные окружения
```
	cd src
	export DATABASE_URL='postgresql://user:password@hostname:port/database_name'
	export SECRET_KEY=????????
```

2. Выполнить миграцию
```
	cd src
	flask db upgrade
```
3. Зполнить базу данных данными из .csv файлов
```
	cd src
	flask create meals
```

После этого можно запустить приложение двумя способами:

1. flask
```
	python3 run.py
```

2. Gunicorn
```
	gunicorn src.app:app
```

Также, с помощью комманд можно создавать новых пользовательей и админов

```
	cd src
	flask create user NAME PASSWORD
	flask create admin NAME PASSWORD
```

Работающее приложения можно посмотреть [тут](https://stepik-flask-course-week-5.herokuapp.com/)

