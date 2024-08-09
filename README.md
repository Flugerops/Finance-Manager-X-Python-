# Finance-Manager
## Introduction
Finance-Manager is a project for the X-Python contest.
Finance-Manager will help you to track your finances by a charting system and much more. </br>
**The application uses [Flask](https://flask.palletsprojects.com/en/3.0.x/) for frontend; [FastAPI](https://fastapi.tiangolo.com/) for backend and [SQLAlchemy](https://www.sqlalchemy.org/) for ORM.** </br>
### Usage: </br>
* You can easily controle your incomes and expenses
* You can compare your finances on different days thanks to graphs
* You're free to delete a transaction if you made a mistake 
## Setup
First of all you need to install ` Docker ` </br>
[``` https://www.docker.com/ ```](https://www.docker.com/) </br>
Then create an `.env` file in application folder </br>
Open it and type: </br>
``` SECRET_KEY = "" ``` And put your secret key like this: `SECRET_KEY = "adA0123MonDa11234mon"` </br>
Then create and start containers:
```
docker compose up
[+] Running 2/0
 ✔ Container finance-manager-x-python--backend-1   Created                                                                                                                                  0.0s 
 ✔ Container finance-manager-x-python--frontend-1  Created                                                                                                                                  0.0s 
Attaching to backend-1, frontend-1
```

Then navigate to:
```
http://127.0.0.1:5000/
```
And your application is **ready!**
