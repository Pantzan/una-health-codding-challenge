# Una Health Backend app

---------------


This is an assigment for Una Health Backend Engineer position.

It is a Python Django REST web app with a API endpoints exposed. 

POST `/api/v1/create_report/` accepts a `report_file` csv file containing the glucose metrics for a single app user and
creates a report objects which appends the given data as metrics in one to many form.

GET `/api/v1/get_levels_by_user/` requires a username in order to fetch the metrics stored for the given user. The 
endpoint accepts basic filtering such as `start`, `end`, `limit` and `sort`. It returns empty if the users has no \
metrics or raises if the user does not exist

GET `/api/v1/get_levels_by_id/$ARG` requires the id arg and fetches the given metric by id

---------------

## Installation instructions

#### Docker:
```
# start the db container and Django app container
make start_containers

# run the initial DB migration
make migrate_docker

# insert the initial user data from fixture
make load_initial_data_docker
```

### Alternatively for local setup:
#### Python and CLI
##### using pyenv
```
pyenv update
pyenv install 3.12.4
pyenv virtualenv 3.12.0 una-app
pyenv local una-app
pip install pip -U
pip install -r requirements.txt
```
##### using venv

```
# make sure you python version is >= 3.9
python -m venv una-app
source una-app/bin/activate
pip install pip -U
pip install -r requirements.txt
```

### Setup and run the app
```
make migrate
make load_initial_data
make run_server
```
## Usage
POST data to the endpoint
### using curl
#### Docker
`curl -X POST 0.0.0.0:8000/api/v1/create_report/ --form report_file="@sample_data/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa.csv"`
##### httpie
`http --form POST 0.0.0.0:8000/api/v1/create_report/ report_file@sample_data/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa.csv`

---------------

#### Local setup
`curl -X POST 127.0.0.1:8000/api/v1/create_report/ --form report_file="@sample_data/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa.csv"`
##### httpie
`http POST 127.0.0.1:8000/api/v1/create_report/ report_file@sample_data/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa.csv`

### run the tests

#### Docker
`make run_tests_docker`
#### local setup
`make run_tests`

## Notes
I chose to use Django REST for the fact that Django provides a robust service out of the box
without much customization. Django's ORM system in my opinion is excellent, fast and flexible.
I decided not to use FastAPI because it will have required more time to achieve what Django offers by default.
The approach is quite straight forward. When the POST request is executed, the corresponding View is responsible for 
3 things. First it makes sure about the POST data integrity. The file is present and contains the given file metadata
such as the report timestamp and the user's name. Next, the view reads the rest of the data in the file and
renames the column names in order to align to English notation based database. Then, it checks if the user exists and 
the report has been pushed before, and it creates the glucose metrics data. We run the transaction as atomic in order
to ensure the database integrity if any of the requests fails to execute or timeout errors. In case of failure, the
transaction will be rolled back. Atomic transaction also ensures that the db will be updated securely from 
a single instance in a swarm of load-balanced instances such as Nginx clusters or Kubernetes clusters.

I decided to use `-1` for storing the missing column data due to inconsistency with pandas NaN filtering and the db
integrity when excepts an int or none values to create the corresponding row.


### challenges
The biggest challenge in the assignment was to ensure the data from csv files will be uniquely parsed from pandas and
fill the NaNs with a negative value.

### improvements
Due to the simplicity and the time limitation, the project does not use any sort of client authorization to ensure
authenticated transactions. Restful authorization such as JWT, OAuth2 or OpenID Connect should be implemented in a
real scenario, production or stage.

The bulk create the metrics is robust, however in the case of thousand oh hundreds of objects to be created at the same
time setting up a fixed `batch_size` value will improve the memory handling. Asynchronous operation in my opinion
could a better approach, however it needs QA testing for verification. 
Django async operations or some sort of instant background tasks service such as Celery will 
improve drastically the request-response cycle and the total overhead of this app. 

### time spend
I spend around 11 hours for this assignment and the polishing around. I wanted to submit a working app which handles
nicely few edge cases and can be streamlined into a staging phase. I also wanted to present to the interviewers how I 
will have implemented a task like that if my team was working on that project and I had a task to create such a service.
I also wanted to demonstrate my problem-solving skills in some depth.
I copied the base part of this app from other active project, so I did not lose time on scaffolding.

### what I could implement if I had few more hours on this assignment
Some sort of validation is necessary for real life scenarios. The file must be validated to be a real csv file and not
a malicious file. Validating its magic numbers it is a good starting point. 

The project also lacks from linting. Although I use pycharm for basic automatic linting, precommit-hooks will have been
a nice addition.

The datetime stored in the db is naive. Some sort of convert into aware it is desired to ensure the timestamps can 
easily convert and used in timezones

Type hints and docstrings. I always use both. Hints are good a docstrings are lifesaver
