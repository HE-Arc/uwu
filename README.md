# uwu
Uwu is the website you need to save your manga reading progress! Just create an account and select all the chapters you have read and add friends to check out their read manga

## Api Django
It is suggested to use a Python virtual environment.

### Api docs
- ReDoc: https://uwu.srvz-webapp.he-arc.ch/api/docs
- Swagger: https://uwu.srvz-webapp.he-arc.ch/api/playground/

### Requirements
- Python

### Setup

#### Dependecies

> If you want to use a virtual environment.
> ```
> # At the root of the project
> 
> # Linux
> python3 -m venv .venv
> # Windows
> python3 -m venv .venv
> ```
> 
> Then activate it.
> ```
> # Linux
> source .venv/bin/activate
> 
> # Windows
> .venv/Scripts/activate
> ```

Install all Dependecies from the `requirement.txt` file.
```
# Linux
# At the root of the project
pip3 install -r requirements.txt

# Windows
pip install -r requirements.txt
```

Run migrations

```
# Linux
cd uwu
python3 manage.py migrate

# Windows
cd uwu
python manage.py migrate
```

Finally run the server
```
# Linux
python3 manage.py runserver

# Windows
python manage.py runserver
```

## VueJs

### Requirement
- NodeJs

### Setup

Install all dependencies
```
# At the root of the project
cd uwuvue
npm install
```

And run the server
```
npm run serve
```
