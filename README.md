# findaplumner

Find a plumber in London. Update the search anytime you want.


## Instalation
*This instructions assumes you have a basic python environment setup on your machine*
*Some uncommon packages you'll need: apt-get install libxml2-dev libxslt1-dev python-dev python-lxml*

The first step is to create a virtualenv and install the requirements

```sh
$ cd path/to/proj
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

If you have any trouble with this, please let me know!

## As a Django app
This Django app in hosted on Heroku and you can visit [here](http://findaplumber.herokuapp.com).
Note that the update link scrapes the website for updated data. To prevent Heroku from timing out, 
a thread was created and 10 second sleep was added. To view all the scraped traders, refresh the page a few seconds after.

To run locally, you can write
```sh
$ python manage.py runserver
```
Make sure you have the virtualenv activated and the proper database settings in the local_settings.py file. This example uses Postgres, so you need that installed on your computer and a database named findaplumber.

If the purpose is only to scrape the data, you can run the following management command:
```sh
$ python manage.py update_plumbers
```

To create your own Heroku app, make sure you have an Heroku account and the [Heroku Toolbelt](https://toolbelt.heroku.com/) installed. 
```sh
$ cd path/to/proj
$ heroku login
$ heroku create appname
$ git push heroku master
$ heroku open
```
You will also need to setup [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql).



## Next steps
* Connect the Scraper to the db to save performance data and stats on each service scraped;
* Improve the tests by randomly saving html pages when scraping and then test over the saved ones;
* Retrieve more data from each trader;
* Analyse the data retrived from each trader and use graphs and stats to draw insights.
* Make the frontend pretty!


