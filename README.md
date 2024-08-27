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
