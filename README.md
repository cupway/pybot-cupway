## PyBot on Heroku

#### What is this?

A Python bot for a [Slack](https://slack.com/) group. It uses the [Python slack client](https://github.com/slackhq/python-slackclient) which is a Python wrapper for the Slack API.

#### Useful Links

* Heroku:
  * [Heroku: Configuration and Config Vars](https://devcenter.heroku.com/articles/config-vars#setting-up-config-vars-for-a-deployed-application)
  * [Dynos and the Dyno Manager: Restarting](https://devcenter.heroku.com/articles/dynos#restarting) 
* Slack:
  * [Slack API](https://api.slack.com/)
  * [Slack API: unfurling (previews)](https://api.slack.com/docs/message-attachments#unfurling)
* Python:
  * [How to Build Your First Slack Bot With Python](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html) -- Tutorial the original skeleton of this bot is based on -- pre customization
  * [Python docs: .format & comma as thousands separator](https://docs.python.org/3/library/string.html#format-specification-mini-language)
  * [Python virtual environments: virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenv) - *"virtualenv is a tool to create isolated Python environments"*
  * [Python `signal` module: handlers for asynchronous events](https://docs.python.org/2/library/signal.html#signal.signal)
* [Game of Thrones quotes API](https://github.com/wsizoo/game-of-thrones-quotes)
  * [GoT API: Quotes storage `.rb` file](https://github.com/wsizoo/game-of-thrones-quotes/blob/master/db/seeds.rb)
* [Unix POSIX signals](https://en.wikipedia.org/wiki/Unix_signal#POSIX_signals)

### Pushing Updates to Heroku

* You must added as a *Collaborator* in the Heroku app config to push updates to the app. 
* Download and install the [Heroku Toolbelt](https://toolbelt.heroku.com/).

Login to Heroku:  
`$ heroku login`

Add the application ([Creating a Heroku remote](https://devcenter.heroku.com/articles/git#creating-a-heroku-remote)):  
`$ heroku git:remote -a pybot-cupway`

Deploy code:  
`$ git push heroku master`

#### Troubleshooting

After pushing, ensure `@pybot` is still *green* in the DMs list (he's online 24/7):  

![foo](images/pybot_green.jpg)

___

If `@pybot` shows offline after pushing to Heroku, there is probably an error in the Python code. Check the Heroku logs:
`$ heroku logs --app pybot-cupway`
___

Sometimes after deploying code, the dyno may stop (usually an indication of a `Traceback` error / issue w/ the Python code). 

After we fix the issue, to start the dyno again after a `git push heroku master` update to Heroku, we can check if the dyno is running (it should try to start automatically, but this indicates no dyno running:

```
$ heroku ps
Free dyno hours quota remaining this month: 550h 0m (100%)
For more information on dyno sleeping and how to upgrade, see:
https://devcenter.heroku.com/articles/dyno-sleeping

No dynos on ⬢ pybot-cupway
```

To manually start it:


```
$ heroku ps:scale worker=1
Scaling dynos... done, now running worker at 1:Free
(venv) 
```
This indicates the Dyno is running:

```
$ heroku ps
Free dyno hours quota remaining this month: 550h 0m (100%)
For more information on dyno sleeping and how to upgrade, see:
https://devcenter.heroku.com/articles/dyno-sleeping

=== worker (Free): python pybot.py (1)
worker.1: up 2016/06/18 23:16:17 -0600 (~ 3s ago)
```
___

Display running Heroku processes:  
`$ heroku ps`

Check Heroku logs (get last 50 lines):  
`$ heroku logs -n 50`

### Heroku Configuration Notes

If you use a new Python library, we have to add it to `requirements.txt` 

Verify the version locally first, so we know what to add to `requirements.txt`:  

```
$ pip freeze
requests==2.10.0
six==1.10.0
slackclient==1.0.0
websocket-client==0.37.0
```
___

In [Heroku Settings](https://dashboard.heroku.com/apps/pybot-cupway/settings), `SLACK_BOT_TOKEN` has to be set as a configuration variable:

![SLACK_BOT_TOKEN config](images/config_vars.jpg)

___

A [`requirements.txt`](https://github.com/cupway/pybot-cupway/blob/master/requirements.txt) file must be in the repo, and it has to reference the Python `slackclient` module, the `requests` module, and any other non "batteries included" Python modules.

### Implementation Notes


From [https://devcenter.heroku.com/articles/dynos#restarting](https://devcenter.heroku.com/articles/dynos#restarting):

> Dynos are also restarted (cycled) at least once per day to help maintain the health of applications running on Heroku. Any changes to the local filesystem will be deleted. The cycling happens once every 24 hours (plus up to 216 random minutes, to prevent every dyno for an application from restarting at the same time). Manual restarts (heroku ps:restart) and releases (deploys or changing config vars) will reset this 24 hour period. 

Heroku sends a `SIGTERM` when the Dyno is cycled, as well as when we run a `$ heroku restart`

Noticed this when reviewing logs:

```
2016-07-01T01:05:15.758436+00:00 heroku[worker.1]: Cycling
2016-07-01T01:05:17.827290+00:00 heroku[worker.1]: Stopping all processes with SIGTERM
2016-07-01T01:05:18.983165+00:00 heroku[worker.1]: Process exited with status 143
2016-07-01T01:05:19.464610+00:00 heroku[worker.1]: Starting process with command `python pybot.py`
2016-07-01T01:05:20.198155+00:00 heroku[worker.1]: State changed from starting to up
2016-07-01T01:05:22.629592+00:00 app[worker.1]: Pybot connected and running
```

`signal_term_handler()` created to gracefully handle `SIGTERM` kill signals.

### Local Dev (Non Heroku)

If we've removed the bot from Heroku, or stopped the `worker` Dyno it's running under and want to test locally, the code is set to pull the bot token from a (per console session) environment variable. 

Set environment variables:  
`$ export SLACK_BOT_TOKEN="put generated token here"`


If using a virtualenv for local Python dev

Install the slack client in the virtualenv:  
`$ pip install slackclient`

Activate the virtualenv for development:  
`$ source bin/activate`


