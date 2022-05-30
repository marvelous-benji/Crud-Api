# Crud-Api
Just a simple API illustrating concepts

#### Technologies

- Python
- Flask
- JWT
- Heroku

[Back To The Top](#read-me-template)

---

## How To Use
API Base URL: https://crud-a.herokuapp.com/api/v1/  

Auth Endpoints: https://crud-a.herokuapp.com/api/v1/auth/register, https://crud-a.herokuapp.com/api/v1/auth/login  

Template Endpoints: https://crud-a.herokuapp.com/api/v1/template

#### Installation
```bash
git clone https://github.com/marvelous-benji/Crud-Api.git
run cd Crud-Api
setup a virtual enviroment by running python -m venv env
then run source env/bin/activate
finally run pip install -r requirements.txt
(check to see if any of these differ on windows OS)
```


#### SetUp

```python
    For Unix(that is mac or linux)
    You can either export the following configurations or create  a config.json file and enter:
    {
    "SECRET_KEY":{Your Secret Key},
    "FLASK_CONFIG":{Set development or production},
    "DEV_DB":{Your mongodb db name},
    "PROD_DB":{Your mongodb db name},
    "TEST_DB":{Your mongodb db name},
    "URI":{Your mongodb url}
    }

    To run test
    pytest -v

    for windows OS use set instead of export

```
