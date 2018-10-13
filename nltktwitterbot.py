import nltk
from TwitterAPI import TwitterAPI


def get_twitter_api():
    # TODO: Remove for public release
    consumer_key = 'gOyKYCNXZhOEzuXCCniFYLqVi'
    consumer_secret = 'rKF7W6gxbt9ArjIrrCRvDwxUBQrRROAvRl5hDHm7cAnOpOcWo6'
    access_token_key = '1051128664631517185-FQhAHJo6WixffqbgIYjXUzYM6YFwO9'
    access_token_secret = 'hUE0TTAdYclgbhPcUxwpPINx326VzCgaqmQf8PMk0s3Ys'
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
    return api


def main():
    print('Starting Up NLTK Twitter Bot')
    # Get Data
    print('Gathering Data...')
    # Train Corpus
    print('Training Corpus...')
    # Evaluate
    # Establish connection with Twitter API
    print('Establish connection with Twitter API...')
    try:
        api = get_twitter_api()

    except Exception:
        print('Connection failed')
        print('Shutting Down NLTK Twitter Bot')
        exit()

    print('Connection Established')
    # Tweet First Tweet
    # r = api.request('statuses/update', {'status': 'This will all end in tears!'})
    # print(r.status_code)

    # Loop:
    # Receive comment
    # Analyse Comment
    # Generate response
    # Tweet response
    print('Shutting Down NLTK Twitter Bot')


main()
