## SimpleTwitterSearch

This was taken with extensive usage from [@tommeagher](http://www.tommeagher.com/)[heroku_ebooks](https://github.com/tommeagher/heroku_ebooks) which in turn uses a lot from: [@harrisj's](https://twitter.com/harrisj) [iron_ebooks](https://github.com/harrisj/iron_ebooks/) Ruby script. I would not have made the slightest progress without these.

## Dependencies

* Python 2.7.16
* python-twitter
* pandas
* tweepy

Running on heroku-18 stack

## Setup

1. Clone this repo
2. Create a dev account and application:
* Create a Twitter account (currently it is only printing to a log file) and 
* Sign into https://dev.twitter.com/apps with the same login and create an application. 
* Make sure that your application has read and write permissions to make POST requests.
3. Copy the consumer key (and secret) and access token (and secret) from your Twiter application and paste them into the appropriate spots in `local_settings.py`. NOTE: YOU SHOULD NOT PASTE THESE FOR EVERYONE TO SEE. YOU may want to put them into an env variable somewhere.
4. Update settings:
* In `local_settings.py`, be sure to add the handle of the Twitter user you want your search account to be based on. 
5. Create an account at Heroku, if you don't already have one. [Install the Heroku toolbelt](https://devcenter.heroku.com/articles/quickstart#step-2-install-the-heroku-toolbelt) and set your Heroku login on the command line.
6. Type the command `heroku create` to generate the simpleTwitterSearch Python app on the platform that you can schedule.
7. The only Python requirement for this script is [python-twitter](https://github.com/bear/python-twitter), the `pip install` of which is handled by Heroku automatically.
8. Commit and push to heroku
* Enter: `git commit -am 'updated the local_settings.py'`
* Enter: `git push heroku master`
9. Test by typing `heroku run worker`. 
10. That's it.


## Configuring

There are several parameters that control the behavior of the bot. You can adjust them by setting them in your `local_settings.py` file. 

```
SEARCHTERM = 'happy'
```
Change this to be the term you want searched by default.

By default, the bot ignores any tweets with URLs in them because those might just be headlines for articles and not text you've written.

## Debugging

If you want to test the script or to debug the tweet generation, you can skip the random number generation and not publish the resulting tweets to Twitter.

First, adjust the `DEBUG` variable in `local_settings.py`.

```
DEBUG = True 
```

After that, commit the change and `git push heroku master`. Then run the command `heroku run worker` on the command line and watch what happens.

If you want to avoid hitting the Twitter API and instead want to use a static text file, you can do that. First, create a text file containing a Python list of quote-wrapped tweets. Then set the `STATIC_TEST` variable to `True`. Finally, specify the name of text file using the `TEST_SOURCE` variable in `local_settings.py`


## Credit
This was taken with extensive usage from [@tommeagher](http://www.tommeagher.com/)[heroku_ebooks](https://github.com/tommeagher/heroku_ebooks) which in turn uses a lot from: [@harrisj's](https://twitter.com/harrisj) [iron_ebooks](https://github.com/harrisj/iron_ebooks/) Ruby script. I would not have made the slightest progress without these. 
I have made significant modifications while little understanding of what I am doing, and thus all errors you find are likely due to me. Feel free to suggest ways to improve the code. Please fork it and send a pull request or file an issue.

## Known Issues
For some reason after running it in terminal, it does not release at the end and so you end up having to restart terminal each time.
