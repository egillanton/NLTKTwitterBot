import nltk
from TwitterAPI import TwitterAPI


def get_twitter_api():
    # TODO: Remove for public release
    consumer_key = ''
    consumer_secret = ''
    access_token_key = ''
    access_token_secret = ''
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
    except ConnectionError:
        print('Connection failed')
        print('Shutting Down NLTK Twitter Bot')
        exit()

    print('Connection Established')
    # Tweet First Tweet

    # Loop:
    # Receive comment
    # Analyse Comment
    # Generate response
    # Tweet response
    print('Shutting Down NLTK Twitter Bot')


main()
