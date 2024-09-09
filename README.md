# FastApi-Projects
commands to run fast api is 
                uvicorn main:app

reaload auto
                uvicorn main:app --reaload

if the main file is inside an app folder then 
                 uvicorn app.main:app --reaload 


good to know
    #whenever we create a new folder for python we create a file __init__.py to add all the packages and we leave it empty for now
    
now about orm
    we use psycopg which usessql to talk to the database and we write that directly in our data base.
    but in orm we dont have to write the sql instead we can write it in python and the orm will convert it into sql.
    instead of manually defining tables in postgres, we can definew our tables as python models.
    queries can be made exclusively through python code. No Sql is necessary.

ORM - SQLALCHEMY
    sqlalchemy is one of the most popular python orms
    when you create a table in order to update it you have to delete and create again

if you want to update without deleting then you have to create tables using alembic

Alembic is a database migration tool
1. We should initialize alembic and we should provide the directory
        alembic init alembic
    this will add alembic to the FASTAPI/alembic directory

2. first import Base from the models file as we want to access all the class from models and not the datbase file
        target_metadata = Base.metadata

3. got alembic.ini
        sqlalchemy.url = postgresql://postgres:Password123@localhost:5432/postgres

4. so the above value wont work if we are using production so we will overide the above step by going to env.py
    under the config
            config.set_main_option("sqlalchemy.url",f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}')

5. alembic revision -m "create post table" this command creates a version

6. in versions ypu can go and checke the  revisions

7.  alembic current : to check the current revision

8.  alembic head: to check the latest revision

9.  alembic upgrade head: to add the changes to the database 

10. alembic downgrade -1: to go back the number of steps needed











NEED to know
    Depends in Fast Api
