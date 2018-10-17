import json
import re
import string

import nltk
from nltk.corpus import stopwords

from Twitter import Twitter


def shutdown_server():
    print('Shutting Down NLTK Twitter Bot')
    exit()


def connect_to_twitter():
    print('Establish connection with Twitter API...')
    try:
        api = Twitter.get_api()
    except Exception:
        print('Connection failed\n')
        shutdown_server()
    print('Connection Established\n')
    return api


def gather_data(api):
    # TODO: DO we want to gather text from Twitter, or from some ready corpus or both?
    print('Gathering Data...')
    sents = []

    # TODO: Gather better Querie Words
    search_queries = ["Píratar",
                      "Framsókn",
                      "Feminismi",
                      "@tmashelgs",
                      "#npc"]

    for q in search_queries:
        print(f'\nGetting Data for: {q}')
        r = api.request('search/tweets', {'q': q})
        for item in r:
            sents.append(item['text'])
            print(f"{item['id']}: {item['text']}")

    return sents


def clean_tweet(a_str):
    if a_str == '':
        return a_str

    a_str = re.sub(r"@[A-z]+\w", '', a_str)
    a_str = re.sub(r"\bhttps:.*\b", '', a_str)
    a_str = re.sub(r"\bRT\b", '', a_str)
    a_str = ''.join([char for char in a_str if char not in string.punctuation])
    a_str = a_str.strip()
    return a_str



def model(api, a_input_str):
    a_input_str = clean_tweet(a_input_str)
    a_input_str_tokens = a_input_str.split()

    # TODO Remove Stop Words
    tokens = [token for token in a_input_str_tokens if token not in stopwords.words('english')]
    tagged_tokens = nltk.pos_tag(tokens)

    # TODO Get Nouns
    noun_set = ["NN", "NNS"]
    NN_words = [word for (word, tag) in tagged_tokens if tag in noun_set]

    # TODO Generate responses for given nouns
    sents = []
    for q in NN_words:
        print(f'Getting Data for: {q}')
        r = api.request('search/tweets', {'q': q,
                                          'lang': 'eng',
                                          'include_entities': 'false',
                                          'result_type': 'recent',
                                          '-filter': 'retweets',
                                          'count': '10'})
        for item in r:
            full_r = api.request('statuses/show/:' + str(item['id']))

            if full_r.status_code == 200:
                tweet = full_r.json()
                text = tweet['text'] if 'text' in tweet else ''
                text = clean_tweet(text)
                if (q,text) not in sents:
                    sents.append((q, text))
        print('Waiting between Requests')

    # TODO return The Most relevant response
    if len(sents) > 0:
        a_output_str = sents[0][1]
    else:
        a_output_str = ''
    return clean_tweet(a_output_str)


def tweet(api, tweet_message):
    r = api.request('statuses/update', {'status': tweet_message})
    print(f'Tweeted:\n{tweet_message}\nwith Status Code: {r.status_code}')
    data = json.loads(r.text)
    return data


def reply_to(api, tweet_message, in_reply_to_status_id):
    r = api.request('statuses/update', {'status': tweet_message, 'in_reply_to_status_id': in_reply_to_status_id})
    print(f'\nTweeted:\n{tweet_message}\nwith Status Code: {r.status_code}')
    # start_time = time.time()
    # if time.time() - start_time > time.time(20):



def main():
    print('Starting Up NLTK Twitter Bot')
    twitter = Twitter()

    my_bot_id = '1051128664631517185'

    # Establishing user stream for my bot
    r = twitter.api.request('statuses/filter', {'follow': my_bot_id})

    # For every activity regarding my bot
    for item in r:
        if 'in_reply_to_user_id_str' in item and item['in_reply_to_user_id_str'] == my_bot_id:
            # Receive data about the sender and the tweet
            sender_tweet_id = item['id'] if 'id' in item else ''
            sender_user_id = item['id_str'] if 'id_str' in item else ''
            sender_user_name = item['user']['screen_name'] if 'user' in item and 'screen_name' in item['user'] else ''
            sender_tweet_text = item['text'] if 'text' in item else ''

            # Analyse Comment
            model_output = model(twitter.api, sender_tweet_text)
            # Generate response
            if sender_user_name != '' and model_output != '':
                my_bot_response = f'@{sender_user_name} {model_output}'
                reply_to(twitter.api, my_bot_response, sender_tweet_id)

    print('Shutting Down NLTK Twitter Bot')


main()

# twitter = Twitter()
# sents = twitter.get_tweets('cars')
# print(f'len(sents): {len(sents)}')
# out = model(api, '@MLVbot: car cat and pineapples https://t.co/m7LvMabAM5')
# print(f'Model Output: \n{out}\n')

