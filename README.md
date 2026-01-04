# 🎓 Senior Project 2025-2026 🎓

### Vulcan Activity Tracker  

![Project Logo](./project_pic/vulcan.png)


# 💡 Project Description:
    "This application aims to use a database and artificial intelligence analysis 
    in order to encourage students to maintain a healthy lifestyle through healthy 
    competition by uploading activities that they have completed into one platform." 


# ⚙️ Technologies & Tools:
    - [Python] 🖥️
    - [Flask] 📚
    - [MSQL or MSSQL] 🗄️
    - [VS Code, Git, GitHub] 🛠️

# IMPORTANT! Run Commands
 ```bash
docker compose up --build  #compile app
 ```
```bash
docker compose up  #start app, ctrl- C to stop
 ```
 ```bash
docker compose down #stop docker
docker compose down -v #clear database volumes
 ```
 ```bash
docker system prune #remove cache
 ```
  - app port is connected to docker

# System Set up

"The following is a guide to folder and file set up for this project. Organization is key to maintaining easy dataflow and development process."

### Folder & File Structure:
 ```bash
sourcecode/
├── server/
│   ├── api/
│   ├── blueprints/
│   └── database/
│
├── templates/
│   ├── base_temp/
│   ├── pages/
│   └── style/
│
├── .gitignore
├── app.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

Server Folder:
- the server folder holds all backend information for the Vulcan Activity Tracker
- it holds all server api endpoints for data propagation and handling
- this folder holds app blueprints and database schema

Folder 1: api
- place server APIs in this folder, here they will connect to javascript reciving APIs on client side
- format = all files ending in .py, named specifically to what service it provides
- import Flask dependancies and libraries needed for data handling
- include blueprint, prefix, and api
- blueprints must be registered in app.py

Example: 
```bash
from flask import Flask, request, jsonify, Blueprint

from argon2 import PasswordHasher

login_api = Blueprint('login_api', __name__) #register in app.py

@login_api.route('/login', methods =['POST'])
```
Folder 2: blueprints
- this folder holds blue.py
- it servers the purpose of initializing folder blueprints and html routes
- html routes must be added to the route dictionary in appropriate format to minimize page rendering
- base template system will be implemented, NO routes hard coded in HTML or JS

Folder 3: controllers
- this folder holds logic for data cleaning and collecting to prepare for database entry
- all dependencies must be initialized 

Folder 4: database
- this folder holds database driving logic
- __init__.py holds logic to create database tables upon app startup
- all creation functions must be called within the __init__ function to minimize confusion
- the following subfolder is crutial to database creation
Schema:
- this folder holds python schema syntax for table creation.
- the python connection, **conn** MUST be passed to creation functions
- this enables the __init__ file to link tables
- in table creation, a table must be checked for existing before creation to improve performance
- all paths must be added

Templates Folder:
- this folder contains all design, style, and page creation logic needed for app
- the system of extending base templates will be used to optimize rendering
- all html files should NOT include javascript code
- javascript should be written in own file, and imported into **html base file**

Folder 1: base_temp
- holds html base page templates for application

Folder 2: pages
- holds html page templates for application

Folder 3: style
- holds 3 components: css, img, js
- custom styles and designs
- images
- javascript logic, reation handling, API 

---
# 🚦 Status:
    [ IN-PROGRESS 🔄 | COMPLETED ✅ | DEMO READY 🎉 ]


# 📅 Timeline:
    - Fall 2025 🍂: Research & Planning
    - Spring 2026 🌸: Implementation & Presentation

# 👥 Group Number:
    ***GROUP #2***

# 📝 Members:
   This project was developed collaboratively by:  
    - **🟢 Margo Bonal**  
    - **🟡 John Gerega**  
    - **🔵 Luke Ruffing**

#✨ Notes:
- recomended VS extentions:
    - Docker (microsoft)
    - Dev Containers (microsoft)
    - WSL (microsoft)
    - SQL Server (mssql) (microsoft)
- recomend running docker through virtual machine for laptop performance saftey
- ssh into vm for code and container editing


==============================
---
### Acknowledgments

We would like to thank everyone who contributed directly or indirectly to the development of this project. Special mentions:  
- 🙏 **Mentors** for guidance and support.  
- 💬 **Peers** for valuable feedback during development.  

💖 Your collaboration and insights are greatly appreciated!
🔥 Let’s make this project awesome! 🔥
