# BOOKYAH Asset Reservation
Simple, elegant asset reservation. Set up categories and assets as an admin, and have users log in to reserve assets. Handy admin dashboard included thanks to the Django framework.

**Link to project:** https://github.com/sineplay/mycal

![Select your asset type - BOOKYAH](https://sineplay.com/wp-content/uploads/bookyah-type.png)

## How It's Made:

**Tech used:** HTML, CSS, JavaScript, Python, Django Framework

Built using the Django framework and FullCalendar, this fine piece of Python script was written out of my immeasurable disappointment in not finding a great asset reservation system without out-of-this-world pricing. I got by with a little help from my AI friend, ChatGPT, as this is my first Python script after writing everyone's favorite starter script, "Hello, World!"

Yes, a leap from outputting text on a terminal to a full-blown asset reservation system does sound a bit outrageous, and you're right. However, that's what happens when I get a little upset about not having what I want and knowing how dangerous I can be to make it happen (just ask my extremely patient wife). I applied my previous knowledge in the basics of programming, intertwined some suggestions and advice from our new AI overlords, and here we have it! Polished top to bottom? *Absolutely not.* Does it function well enough for my needs? You bet it does. I hope it works for you, too. If not, as we say about the weather here in Massachusetts, just wait a little while. The next revision might be somewhat better.

## Optimizations

This thing has no optimizations yet. I kinda just finished a functioniong app at the time of writing this README. Stay tuned.

## Prerequesites

- Python 3.8
- Mail server

The following Python packages are also needed, and are found in requirements.txt.
- Django 4.2.6
- Django-widget-tweaks
- Python-decouple 3.8

## Installation

1. Clone the main branch to your computer.
2. At the root level of the app, in the mycal folder, create a file named ".env" with the following settings (only EMAIL_HOST and EMAIL_PORT are required):
- EMAIL_HOST=
- EMAIL_PORT=
- EMAIL_USE_TLS=(True/False)
- EMAIL_HOST_USER=
- EMAIL_HOST_PASSWORD=
3. Open a terminal / command prompt, navigate to the folder with the requirements.txt file, and run the command:
```
pip install -r requirements.txt
```
4. Change to the mycal directory in the terminal / command prompt.
5. Run the following command to start the server:
```
python manage.py runserver
```

If all goes well, your BOOKYAH asset reservation app should be live on your host at http://localhost:8000. Enjoy!
