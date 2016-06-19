### PyBot on Heroku

#### Useful Links

* [Heroku: Configuration and Config Vars](https://devcenter.heroku.com/articles/config-vars#setting-up-config-vars-for-a-deployed-application)
* [Slack API](https://api.slack.com/)
* [How to Build Your First Slack Bot With Python](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html) -- Tutorial this bot is based on

### Pushing Updates to Heroku

Need to be a *Collaborator* in the Heroku app config.

Download the [Heroku Toolbelt](https://toolbelt.heroku.com/)

Login to Heroku:  
`$ heroku login`

Add the application ([Creating a Heroku remote](https://devcenter.heroku.com/articles/git#creating-a-heroku-remote)):  
`$ heroku git:remote -a pybot-cupway`

Deploy code:  
`$ git push heroku master`

Start the dyno again after a `git push heroku master` update to Heroku:  

```
$ heroku ps
Free dyno hours quota remaining this month: 550h 0m (100%)
For more information on dyno sleeping and how to upgrade, see:
https://devcenter.heroku.com/articles/dyno-sleeping

No dynos on ⬢ pybot-cupway
(venv) 
```

That indicates no dyno running. Let's start it:


```
$ heroku ps:scale worker=1
Scaling dynos... done, now running worker at 1:Free
(venv) 

$ heroku ps
Free dyno hours quota remaining this month: 550h 0m (100%)
For more information on dyno sleeping and how to upgrade, see:
https://devcenter.heroku.com/articles/dyno-sleeping

=== worker (Free): python pybot.py (1)
worker.1: up 2016/06/18 23:16:17 -0600 (~ 3s ago)
```

Display running Heroku processes:  
`$ heroku ps`

### Configuration Notes

In [Heroku Settings](https://dashboard.heroku.com/apps/pybot-cupway/settings), `SLACK_BOT_TOKEN` has to be set as a configuration variable:

![SLACK_BOT_TOKEN config](images/config_vars.jpg)

`requirements.txt` referencing the Python `slackclient` module is needed.


### Local Dev (Non Heroku)

If we've removed the bot from Heroku, or stopped the `worker` Dyno it's running under and want to test locally, the code is set to pull the bot token from a (per console session) environment variable. 

Set environment variables:  
`$ export SLACK_BOT_TOKEN="put generated token here"`


If using a virtualenv for local Python dev, activate it:  
`$ source bin/activate`


