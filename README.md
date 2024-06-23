# BOOKYAH Asset Reservation
Simple, elegant asset reservation. Set up categories and assets as an admin, and have users log in to reserve assets. Handy admin dashboard included thanks to the Django framework.

**Link to project:** https://github.com/sineplay/bookyah

![Select your asset type - BOOKYAH](https://sineplay.com/wp-content/uploads/bookyah-type.png)

## How It's Made:

**Tech used:** HTML, CSS, JavaScript, Python, Django Framework

Built using the Django framework and FullCalendar, this fine piece of Python script was written out of my immeasurable disappointment in not finding a great asset reservation system without out-of-this-world pricing. I got by with a little help from my AI friend, ChatGPT, as this is my first Python script after writing everyone's favorite starter script, "Hello, World!"

Yes, a leap from outputting text on a terminal to a full-blown asset reservation system does sound a bit outrageous, and you're right. However, this is something I took absolute pride in to develop. I applied my previous knowledge in the basics of programming, intertwined some suggestions and advice from our new AI overlords, and here we have it! Polished top to bottom? *Absolutely not.* Does it function well enough for my needs? You bet it does. I hope it works for you, too. If not, as we say about the weather here in Massachusetts, just wait a little while. The next revision might be somewhat better.

## Optimizations

This thing has no optimizations yet. I kinda just finished a functioning app at the time of writing this README. Stay tuned.

## Prerequesites

- Python 3.8
- Mail server

The following Python packages are also needed, and are found in requirements.txt.
- Django 4.2.6
- Django-widget-tweaks
- Python-decouple 3.8

## Automatic Installation

1. Clone the main branch to your computer.
2. Start the setup script:

**Linux/Mac:**
From Terminal/Bash (you may need to add execute permissions first: chmod +x setup.sh):
```
./setup.sh
```
**Windows:**
From PowerShell:
```
.\setup.ps1
```
3. Follow the instructions in the script (enter your Superuser details).
4. After the script completes, update your .env file (mycal/.env) with your own email server values.
5. **Important:** Once completed with testing, and especially for production environments, turn off debug mode. In mycal/mycal/settings.py, update the following line:
```
DEBUG = True
```
To:
```
DEBUG = False
```

## Manual Installation

1. Clone the main branch to your computer.
2. At the root level of the app, in the mycal folder, rename ".env.example" to ".env".
3. Modify .env with your own values. For SECRET_KEY, you can use the Django admin shell to generate a key (do not share or use with any other installation) - steps provided below.
4. Open a terminal / command prompt, navigate to the root of the BOOKYAH folder, and create a virtual environment:
```
python -m venv venv
```
5. Activate the virtual environment:

**Linux/Mac:**
```
source venv/bin/activate
```
**Windows:**
```
venv\scripts\activate
```
6. Install required Python plugins:
```
pip install -r requirements.txt
```
7. **Important:** Once completed with testing, and especially for production environments, turn off debug mode. In mycal/mycal/settings.py, update the following line:
```
DEBUG = True
```
To:
```
DEBUG = False
```

## Generate a SECRET_KEY (for manual installations)

This requires that you've already installed Python, created a virtual environment, and installed the plugins.

1. With the virtual environment activated, in terminal / command prompt, start Python
```
python
```
2. Enter the following line:
```
from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())
```

The output on the line following the command (long string of random characters) is your SECRET_KEY.

## Start the BOOKYAH server

1. Open a terminal / command prompt, navigate to the root of the BOOKYAH folder, and start the virtual environment (if not already activated):
```
source venv/bin/activate
```
2. Start the server:
```
python mycal/manage.py runserver
```

BOOKYAH should now be accessible at the default port (http://localhost:8000). Log in with the superuser account you created during the setup. Enjoy!

## Install BOOKYAH on a web server ##

Instructions above are mainly for testing on a local machine. If you're ready to rock and roll in production, please follow the steps in the Wiki: [Install BOOKYAH on a Linux Web Server (nginx)](https://github.com/sineplay/bookyah/wiki/Install-BOOKYAH-on-a-Linux-Web-Server-(nginx))

## Donate

Enjoy the app? Feel the uncontrollable desire to contribute to my big dreams? As the founder of Sineplay Studios, LLC, I invite you to [donate via PayPal](https://www.paypal.com/donate/?hosted_button_id=4CKBM3N63AXJE), and you will have my ultimate thanks in return.

## License

This software is governed by the [GNU GPL](LICENSE).
