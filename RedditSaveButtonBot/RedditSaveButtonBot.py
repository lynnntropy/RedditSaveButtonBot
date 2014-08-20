import praw
from datetime import datetime
import calendar
import time

login_file = open('login.txt')
login_data = login_file.readlines()
login_file.close()

username = login_data[0].strip()
password = login_data[1].strip()
reddit = praw.Reddit(user_agent='Reddit Save Button Bot by /u/OmegaVesko')
reddit.login(username, password)

subreddit_to_track = 'all'
patterns = ['.', 'save', 'saved']
#patterns = ['trigger_save_button_bot']

reply_body = """Hey there! It looks like you're trying to save something on Reddit by replying to it.
You probably missed the 'save' button Reddit puts below every post and comment. Hit that and it'll show up on the 'saved' tab on your
front page. Easy as that!

Trying to save a comment on a mobile app that doesn't support it? 
[Reddit News](https://play.google.com/store/apps/details?id=free.reddit.news&hl=en) (Android) and 
[Readit](http://www.windowsphone.com/en-us/store/app/readit/77ca2a13-7a17-43bb-84c4-1cba1e514b78) (Windows Phone) 
are both amazing apps that make saving comments a breeze.

Still having trouble, or don't want to switch apps? [Pocket](http://getpocket.com/) is a great service 
that lets you save anything at all in the cloud, not just Reddit posts/comments."""

print "<< Starting comment tracking for /r/%s >>\n" % subreddit_to_track

for comment in praw.helpers.comment_stream(reddit, subreddit_to_track, limit=None, verbosity=0): # indefinite comment stream!

    current_time_unix = int(time.time())

    time_difference = current_time_unix - comment.created_utc # in seconds

    # limit search to comments less than 5 minutes old
    if time_difference < 5 * 60: 

        # check if the comment matches one of the patterns
        if comment.body.strip() in patterns:

            # found a matching comment!
            print "\nMatching comment submitted %d seconds ago to /r/%s!\n '%s' by /u/%s" % (time_difference, subreddit_to_track, comment.body[:15], comment.author)

            try:
                comment.reply(reply_body)
                print "   Replied to comment."
            except:
                print "   Tried to comment but Reddit replied 'you're doing that too much'."
