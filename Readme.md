#Brightwheel Interview Test

7/12/17

Author: Kevin Johnson

This project uses Python 2.7 and Django to provide an interface to Mailgun and Sendgrid mailing APIs.

The project is hosted on Heroku's free plan which has a constraint where the project will go to "sleep" after no use over 15 
minutes. This just means that the first time you make a request to the URL, it may take longer to load than usual while
the project "wakes up". It is recommended to go to the main site before attempting any manual post requests.

###Links
Project description can be found at: https://d2gn4xht817m0g.cloudfront.net/conversation_message_attachment/i/199260-a264b25209b4ca6a860dd5cc844bd748-original?1499272678

The main site is live at: https://brightwheel-test.herokuapp.com/

The endpoint can be accessed at: https://brightwheel-test.herokuapp.com/email/

## Installation

It's best to run these projects from a virtual python environment instead of your main one due to project-specific 
dependencies. If you don't have it installed, run `pip install virtualenvwrapper` from a terminal to install a useful 
tool.

Once installed, move your directory to the base brightwheel folder in this project and run these commands to create a 
new virtual environment and install the required dependencies.
1. `mkvirtualenv brightwheel-kj`
2. `workon brightwheel-kj`
3. `pip install -r requirements.txt`

### Running The Service
If you'd like to run the project locally, you can open a terminal in the project directory and enter the following 
commands:
1. `workon brightwheel-kj` (If it isn't already activated)
2. `python manage.py run_server`

You should then be able to access the service by making a post request to `127.0.0.1:8000/email/` with the appropriate 
data.

## Libraries & Frameworks

### Django
Django is the main framework the website is running on. Django is a great Python web development framework that is very 
extensible. It is primarily used for project structure and URL routing in this example.

Django-extensions is a supplementary library that adds some handy utility features to Django. I like using 
`python manage.py shell_plus` as a convenient way of bringing up a more robust Django terminal.

### Requests
Requests is a very popular Python library for making HTTP requests. It is very extensible and easily handles the Mailgun
and Sendgrid Web APIs.

### Waitress
Waitress is the production ready server we use. Heroku actually recommends you use Gunicorn here but
Gunicorn isn't recommended for public facing servers.