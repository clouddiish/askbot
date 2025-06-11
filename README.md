# askbot

askbot is a `discord.py` bot implementing various functionalities useful for my friendgroup discord server, self-hosted on raspberry pi

## features

- setting user's birthdays, reminder when it's somebody's birthday
- periodic automatic creation of polls on when to hang out
- checking for who is playing on a related minecraft server and updating voice channels to reflect that
- setting and receiving reminders

## getting started

### dependencies

- working discord server with sufficient privileges
- account and an application with bot in [discord's developer portal](http://discordapp.com/developers/applications)
- Python 3.8 or later
- Python packages from `requirements.txt`

```
pip install -r requirements.txt
```

### installation

- clone the repository or download the code files
- copy the `.env-example` file to `.env` and fill in the required environmental variables

### run

- to run the project locally, run the below command

```
python -m bot
```

- to run the script on your raspberry pi, adjust and run the `start.sh` script

```
/bin/bash /path/to/start.sh
```

### run tests

- run the tests with the below command

```
python -m pytest
```
