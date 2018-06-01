## Dependencies

I recommend you use [pipenv](https://github.com/pypa/pipenv).
```
pipenv install
pipenv shell
```

## Project setup

Now sync your database for the first time.
```
python manage.py migrate
```
Create an initial user named admin with a password of password123.
```
python manage.py createsuperuser --email admin@example.com --username admin
```

##Testing our API

You're now ready to test the API.
```
python manage.py runserver
```

You can easily test if the endpoint is working by doing the following in your terminal
```
curl -X POST -d "username=admin&password=password123" http://localhost:8000/api/token-auth/

```
Now in order to access protected api urls you must include the Authorization: Bearer <your_token> header.
```
curl -H "Authorization: Bearer <your_token>" http://localhost:8000/api/transactions/

```
More details about endpoints access [documentation](http://localhost:8000/docs/).
