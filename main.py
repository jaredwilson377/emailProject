import os
import time
import logging
import mailslurp_client
import tweepy
#
configuration = mailslurp_client.Configuration()
configuration.api_key['x-api-key'] = os.getenv("api_key_mail")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()



def sendTweet():
    logger.info("Sending tweet")
    api = tweepy.Client(bearer_token=os.getenv("bearertoken"),
                        access_token=os.getenv("accesstoken"),
                        access_token_secret=os.getenv("accesstokensecret"),
                        consumer_key=os.getenv("key"),
                        consumer_secret=os.getenv("secret"))
    api.create_tweet(text='My Ventra card just auto-reloaded!\n\n(This action was performed by a bot.) '
                      'https://github.com/jaredwilson377')




def driver():
    logger.info("Waiting...")
    with mailslurp_client.ApiClient(configuration) as api_client:
        inbox_controller=mailslurp_client.InboxControllerApi(api_client)
        emails = inbox_controller.get_emails(os.getenv("inboxId"))
        for email in emails:
            if(email._from == "updates@ventrachicago.com" and  email.subject == "Ventra Threshold Autoload Receipt"):
                sendTweet()
    inbox_controller.delete_all_inbox_emails(os.getenv("inboxId"))
    logger.info("Inbox cleared")

if __name__ == '__main__':

    while True:
        driver()
        time.sleep(500)
