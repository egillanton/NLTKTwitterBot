import nltk
import json
import Twitter


def shutdown_server():
    print('Shutting Down NLTK Twitter Bot')
    exit()


def connect_to_twitter():
    print('Establish connection with Twitter API...')
    try:
        api = Twitter.get_api()
    except Exception:
        print('Connection failed')
        shutdown_server()
    print('Connection Established')
    return api


def gather_data(api):
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


def tweet(api, tweet_message):
    r = api.request('statuses/update', {'status': tweet_message})
    print(f'Tweeted:\n{tweet_message}\nwith Status Code: {r.status_code}')
    data = json.loads(r.text)
    my_comment_id = data['id']
    return my_comment_id 


def reply_to(api, tweet_message, in_reply_to_status_id):
    r = api.request('statuses/update', {'status': tweet_message, 'in_reply_to_status_id': in_reply_to_status_id})
    print(f'Tweeted:\n{tweet_message}\nwith Status Code: {r.status_code}')


def main():
    print('Starting Up NLTK Twitter Bot')

    api = connect_to_twitter()

    #sents = gather_data(api)

    # Train Corpus
    # print('Training Corpus...')
    # Evaluate

    # Tweet First Tweet
    tweet_message = 'Hello, is anybody out there?'
    my_tweet_id = tweet(api, tweet_message)


    my_bot_id = '1051128664631517185'

    # Loop async
    r = api.request('statuses/filter', {'follow': my_bot_id})
    for item in r:
        if 'in_reply_to_user_id_str' in item and item['in_reply_to_user_id_str'] == my_bot_id:
            # Receive tweet
            message_id = item['id'] if 'id' in item else ''
            sender_id = item['id_str'] if 'id_str' in item else ''
            text = item['text'] if 'text' in item else ''
            username = item['user']['screen_name'] if 'user' in item  and 'screen_name' in   item['user'] else ''
            # Analyse Comment
            # Generate response
            response = 'Ohh Hello there, thanks for noticing me!'
            if username != '':
                new_response =  f'@{username} {response}'
                # Tweet response
                reply_to(api, new_response, message_id)


    print('Shutting Down NLTK Twitter Bot')

main()
