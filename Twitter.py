from TwitterAPI import TwitterAPI, TwitterPager
import json


class Twitter:
    __consumer_key = 'gOyKYCNXZhOEzuXCCniFYLqVi'
    __consumer_secret = 'rKF7W6gxbt9ArjIrrCRvDwxUBQrRROAvRl5hDHm7cAnOpOcWo6'
    __access_token_key = '1051128664631517185-FQhAHJo6WixffqbgIYjXUzYM6YFwO9'
    __access_token_secret = 'hUE0TTAdYclgbhPcUxwpPINx326VzCgaqmQf8PMk0s3Ys'
    __user_id_str = '1051128664631517185'

    def __init__(self):
        print('Establish connection with Twitter API...')

        try:
            self.api = TwitterAPI(self.__consumer_key,
                                  self.__consumer_secret,
                                  self.__access_token_key,
                                  self.__access_token_secret)
        except Exception:
            print('Connection failed\n')
        self.user_id_str = self.__user_id_str

        print('Connection Established\n')

    def get_tweets(self, q, count=5):
        tweets = []
        r = TwitterPager(self.api, 'search/tweets', {'q': q, 'count': count})
        for item in r.get_iterator():
            if 'text' in item:
                tweets.append(item['text'])
            elif 'message' in item and item['code'] == 88:
                print
                'SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message']
                break
        return tweets

    def tweet(self, tweet_message):
        r = self.api.request('statuses/update', {'status': tweet_message})
        print(f'Tweeted:\n{tweet_message}\nwith Status Code: {r.status_code}')
        data = json.loads(r.text)
        return data

    def reply_message_to(self, tweet_message, in_reply_to_status_id):
        r = self.api.request('statuses/update', {'status': tweet_message, 'in_reply_to_status_id': in_reply_to_status_id})
        print(f'\nTweeted:\n{tweet_message}\nwith Status Code: {r.status_code}')

    def get_user_stream(self):
        return self.api.request('statuses/filter', {'follow': self.user_id_str})
