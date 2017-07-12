# Brightwheel Interview Test

7/12/17

Author: Kevin Johnson

This project uses Python 2.7 and Django to provide an interface to Mailgun and Sendgrid mailing APIs.

The project is hosted on Heroku's free plan which has a constraint where the project will go to "sleep" after no use over 15 
minutes. This just means that the first time you make a request to the URL, it may take longer to load than usual while
the project "wakes up". 

**It is recommended to go to the main site before attempting any manual post requests**.

Note: There is a configuration variable, MAIL_ACTIVE, which can be used to set the default mail service. This is defined
in Heroku's environmental variables. 

### Links

* [Project Description](https://d2gn4xht817m0g.cloudfront.net/conversation_message_attachment/i/199260-a264b25209b4ca6a860dd5cc844bd748-original?1499272678)
* [Main Site and Form](https://brightwheel-test.herokuapp.com/)
* [Endpoint](https://brightwheel-test.herokuapp.com/email/) (POST only)

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
data or directly going to `127.0.0.1:8000` for the entry form.

### Running The Tests
We use pytest to test the project before deploying. In order to run the tests, make sure you're in the project driectory 
and run `pytest --ds=settings`

## Libraries and Frameworks

### Django
Django is the main framework the website is running on. Django is a great Python web development framework that is very 
extensible. It is primarily used for project structure and URL routing in this example.

Django-extensions is a supplementary library that adds some handy utility features to Django. I like using 
`python manage.py shell_plus` as a convenient way of bringing up a more robust Django terminal.

### Pytest
Pytest is used to test the project. It also uses an addon, pytest-django, with some helpers specific to Django.
The tests can be found in `main/main_test.py` which tests the endpoint with various parameters and expected results on
both services.

### Requests
Requests is a very popular Python library for making HTTP requests. It is very extensible and easily handles the Mailgun
and Sendgrid Web APIs.

### Waitress
Waitress is the production ready server we use. Heroku actually recommends you use Gunicorn here but
Gunicorn isn't recommended for public facing servers.

## Tradeoffs and Improvements

1. One of the biggest problems I see with this is that it is synchronous. Every request sent to the endpoint must wait
for another request to be sent to the provider. Ideally the endpoint would add the message to a Queue immediately and with
another worker iterate through the queue and send messages. This could be done with a simple CRON job, or the Heroku 
Scheduler Plugin since the site is already hosted on that.

2. Since these are tied to my own accounts on Sendgrid and Mailgun, I don't want a random person taking advantage and
sending thousands of emails on my behalf. Two ways to remedy that would be by adding authentication and rate limiting.
If the user has to sign in before use, I can remove access from any offending users. To do this I'd likely use the
[Django Rest Framework](http://www.django-rest-framework.org/). 

3. Depending on usage it may be useful to add the possibility of bulk sending. This would be great for users
with a high volume of messages. Sendgrid allows up to 1000 recipients on each email.

4. Mailgun and Sendgrid also offer extensive APIs for feedback and analytics on your emails. It would be interesting to 
incorporate these into the project.

5. Final note is that emails from Mailgun seem to end up in the Spam folder usually while Sendgrid makes it through.
This may be because Mailgun has you specify your own domain to send from while Sendgrid uses its own.


