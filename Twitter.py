from TwitterAPI import TwitterAPI, TwitterPager


class Twitter:
    __consumer_key = 'gOyKYCNXZhOEzuXCCniFYLqVi'
    __consumer_secret = 'rKF7W6gxbt9ArjIrrCRvDwxUBQrRROAvRl5hDHm7cAnOpOcWo6'
    __access_token_key = '1051128664631517185-FQhAHJo6WixffqbgIYjXUzYM6YFwO9'
    __access_token_secret = 'hUE0TTAdYclgbhPcUxwpPINx326VzCgaqmQf8PMk0s3Ys'

    def __init__(self):
        self.api = TwitterAPI(self.__consumer_key,
                              self.__consumer_secret,
                              self.__access_token_key,
                              self.__access_token_secret)

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
