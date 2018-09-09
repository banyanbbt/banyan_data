# Banyan Data

Banyan Data has been launched in Chinese. Community users can participate in data governance by receiving data collection tasks, cleaning tasks, and tagging tasks.

Official website [Banyan Data](http://data.banyanbbt.org "Banyan Data")

## What's included


Within the download you'll find the following directories and files, logically grouping common assets and providing both compiled and minified variations. You'll see something like this:


```

banyan_data/
├── apps
├── config
├── banyan_data
├── lib
├── log
├── media
├── static
├── templates
├── manage.py
├── README.md
├── requirements.txt

```


## Getting started


1. Requirements

```

Ubuntu 16.x
Python 3.6.x
Django 2.0.7
MySQL 5.7.x

```

Banyan Data applications require python 3.6+ and MySQL 5.7+, and works with both Mac OS X or Linux. While in theory it should work on Windows, it has never been tried.


2. Installation

```

mkvirtualenv banyan_data

workon banyan_data

pip install -r requirements.txt

CREATE DATABASE IF NOT EXISTS banyan_data DEFAULT CHARACTER SET utf8mb4;

python manage.py migrate


nohup python manage.py runserver 0.0.0.0:8000  &

nohup celery -A config worker -l info --logfile log/celery.log &

nohup celery -A config beat -l info  --logfile log/celery_beat.log &


```

    Go to `http://localhost:8000` and you'll see the Banyan Data project's website.



