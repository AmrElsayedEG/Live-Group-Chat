## Asynchronous Group Chat [Real-Time] ![Django](https://img.shields.io/badge/Django-2.2.9-yellow.svg) ![Django](https://img.shields.io/badge/Django%20channels-3.0.2-green.svg)


## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Run](#run)

## General info
- This project provides you to create private real-time group chat, You can enter the group name and your name to join others.
- No messages saved in the database so when you end your session the messages disappear forever.
- You can see the number or online users in your group chat and also see when user join or leave your channel.
- This project built using Django and Django Channels (WebSockets) so it's completely asynchronous application.

## Technologies
Project is created with:
* Django: 2.2
* Django Channels: 3.0
* Twisted: 20.3
	
## Run
To run this project, install it locally and make sure to install the twisted version that can run with your os with no problem
Here is the Twisted v20.3.0 for windows, You will find the file in the repo

```
$ pip install requirements.txt
$ python manage.py runserver
```

After running the server make sure to run the redis server located inside [redis/redis-server.exe]
