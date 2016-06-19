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