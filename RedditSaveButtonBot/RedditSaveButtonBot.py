import praw
import time

login_file = open('login.txt')
login_data = login_file.readlines()
login_file.close()

username = login_data[0].strip()
password = login_data[1].strip()
reddit = praw.Reddit(user_agent='Reddit Save Button Bot by /u/OmegaVesko')

reddit.config._ssl_url = None # disable SSL because it messes up PythonAnywhere
reddit.login(username, password)

subreddit_to_track = 'all'
patterns = ['.', 'save', 'saved']
#patterns = ['trigger_save_button_bot']

special_loop_count = 10000

reply_body = """Hey there! It looks like you're trying to save something on Reddit by replying to it.
You probably missed the 'save' button Reddit puts below every post and comment. Hit that and it'll show up on the 'saved' tab on your
front page. Easy as that!

Trying to save a comment on a mobile app that doesn't support it? 
[Reddit News](https://play.google.com/store/apps/details?id=free.reddit.news&hl=en) (Android) and 
[Readit](http://www.windowsphone.com/en-us/store/app/readit/77ca2a13-7a17-43bb-84c4-1cba1e514b78) (Windows Phone) 
are both amazing apps that make saving comments a breeze.

Still having trouble, or don't want to switch apps? [Pocket](http://getpocket.com/) is a great service 
that lets you save anything at all in the cloud, not just Reddit posts/comments.

====

^this ^comment ^will ^be ^deleted ^automatically ^if ^its ^score ^is ^-1 ^or ^lower."""

print "<< Starting comment tracking for /r/%s >>\n" % subreddit_to_track

i = 0

for comment in praw.helpers.comment_stream(reddit, subreddit_to_track, limit=None, verbosity=0): # indefinite comment stream!
    
    i += 1

    if i >= special_loop_count:
        i = 0
        # run the 'special loop' without interrupting comment parsing 
        print "\n-- Running 'special' loop --"

        my_user = praw.objects.LoggedInRedditor(reddit, user_name=username)

        deleted_comment_count = 0

        for comment in my_user.get_comments(limit=None):
            if comment.score < 0:
                deleted_comment_count += 1
                print "Deleting comment in %s with score %d" % (comment.subreddit.url, comment.score)
                comment.delete()

        print "-- Special loop finished. %d comments deleted. --" % deleted_comment_count


    current_time_unix = int(time.time())

    time_difference = current_time_unix - comment.created_utc # in seconds

    # limit search to comments less than 5 minutes old
    if time_difference < 5 * 60: 

        # check if the comment matches one of the patterns
        if comment.body.strip() in patterns:

            parent_comment = reddit.get_info(thing_id=comment.parent_id)            

            # found a matching comment!
            print "\nMatching comment submitted %d seconds ago to %s!\n '%s' by /u/%s" % (time_difference, comment.subreddit.url, comment.body[:15], comment.author)

            if parent_comment.author.name == 'SaveButtonReminder':
                try:
                    comment.reply("Nice try.")
                    print "   Replied 'nice try' to comment."
                except:
                    print "   Tried to reply 'nice try' but Reddit replied 'you're doing that too much'."
            else:
                try:
                    comment.reply(reply_body)
                    print "   Replied to comment."
                except:
                    print "   Tried to comment but Reddit replied 'you're doing that too much'."
