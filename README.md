# PizzaPyRobot
I used to work next to Stobies' Pizza, a local pizza shop that ran a ‘name of the day’ promotion. Every day they would randomly choose two names, and anyone who had one of those names would get free pizza. The shop wrote the names on a chalkboard and they’d also tweet out the names at roughly the same time every day. This gave me an idea; what if there was a script that would periodically read the shop’s tweets, and direct message co-workers and friends on Slack if they have a winning name that day? Well, now there is.

To run this code you'll need: 
* A [twitter developer account](https://developer.twitter.com)
  * Which will give you the `CONSUMER_KEY`, `CONSUMER_SECRET`, `ACCESS_TOKEN`, and `ACCESS_TOKEN_SECRET` needed to communicate with the Twitter API.
* Create a [Slack Bot](https://api.slack.com/bot-users#creating-bot-user) to get a `BOT_KEY`.
  * This will allow the bot to slack people in your channel.

Finally, you can use the [serverless](https://medium.com/faun/aws-lambda-serverless-framework-python-part-1-a-step-by-step-hello-world-4182202aba4a) package, and the [serverless-python-requirments](https://serverless.com/blog/serverless-python-packaging/) plugin to deploy the script as an AWS Lambda. This will allow also you to create a custom cron to check for winners periodically.
