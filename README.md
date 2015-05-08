DRFbot
======

[@DRFbot](https://twitter.com/DRFbot) is my dear bot on Twitter.


How to revive it
----------------

Execute _bot.sh_ in your Linux computer.
_bot.sh_ checks if the bot process is working or not.
It does nothing if the bot process is working, sets up the bot if not.

Insert a following line in your crontab.

```
*/1 * * * * /path/to/drfbot/bot.sh
```
