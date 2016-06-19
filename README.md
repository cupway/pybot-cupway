### PyBot on Heroku

[Heroku: Configuration and Config Vars](https://devcenter.heroku.com/articles/config-vars#setting-up-config-vars-for-a-deployed-application)

Download the [Heroku Toolbelt](https://toolbelt.heroku.com/)

Login to Heroku:  
`$ heroku login`

Add the application:  
`$ heroku git:remote -a pybot-cupway`

If using a virtualenv, activate it:  
`$ source bin/activate`

Set environment variables:  
`$ export SLACK_BOT_TOKEN="put generated token here"`

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