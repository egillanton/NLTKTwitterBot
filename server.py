import os
import sys
import glob
import copy
from tqdm import trange
from nltk import ConditionalFreqDist
from Twitter import Twitter


def get_corpus_from_file(path):
    file_names = glob.glob(os.path.join(path, '*.txt'))
    corpus = []
    t = trange(len(file_names), desc='Creating Corpus')
    for i in t:
        fin = open(file_names[i], 'r', encoding='utf-8')
        tokens = []
        punctuations = [".", ",", ";", ":", "?", "!"]
        for line in fin:
            if line.strip() and line.split()[0].strip() not in punctuations:
                tokens.append(line.split()[0].strip())
            else:
                corpus.append(copy.deepcopy(tokens))
                tokens = []
        sys.stdout.flush()
    return corpus


def get_ngram(corpus, n):
    ngram = []
    t = trange(len(corpus), desc=f'Creating {n}-gram')
    for i in t:
        sequences = [corpus[i][j:] for j in range(n)]
        ngram.extend(list(zip(*sequences)))
    sys.stdout.flush()
    return ngram


def get_conditional_freq_dist(ngram):
    t = trange(len(ngram), desc=f'Creating Conditional frequency distributions for {len(ngram[0])}-gram')
    condition_pairs = []
    for i in t:
        words = ngram[i]
        condition_pairs.append((tuple(words[:-1]), words[-1]))
    return ConditionalFreqDist(condition_pairs)


def generate_sent(cdf, words, max_words):
    first_word = words[0]
    question_starters = ['er', 'hver', 'hverjir', 'hverjar', 'hvert', 'hvað', 'hvern', 'hverja', 'hverjum', 'hverri',
                         'hverju', 'hvers', 'hverra', 'hverrar']
    a_str = ''
    a_str += first_word.title() + ' '
    a_str += ' '.join([word for word in words[1:-1]])
    n = len(cdf.conditions()[0])
    for i in range(max_words):
        a_str += words[-1]
        try:
            words = words[-(n-1):] + [cdf[tuple(words[-n:])].max()]
        except ValueError:
            break
        if not i == max_words - 1:
            a_str += ' '
    if first_word in question_starters:
        a_str += '?"'
    else:
        a_str += '."'
    return a_str


def main():
    path = './data/IFD1_SETS'
    corpus = get_corpus_from_file(path)
    ngram = get_ngram(corpus, 3)
    cdf = get_conditional_freq_dist(ngram)

    print('Testing out CDF')
    words = ['er', 'þetta']
    sent = generate_sent(cdf, words, 15)
    print(f'Generated Text from the words {words}:\n{sent}')

    print('Starting Up Twitter Bot')
    twitter = Twitter()

    # Establishing user stream for my bot
    for item in twitter.get_user_stream():
        if 'in_reply_to_user_id_str' in item and item['in_reply_to_user_id_str'] == twitter.user_id_str:
            # Receive data about the sender and the tweet
            sender_tweet_id = item['id'] if 'id' in item else ''
            sender_user_id = item['id_str'] if 'id_str' in item else ''
            sender_user_name = item['user']['screen_name'] if 'user' in item and 'screen_name' in item['user'] else ''
            sender_tweet_text = item['text'] if 'text' in item else ''

            # Analyse Comment
            # model_output = model(twitter.api, sender_tweet_text)
            model_output = ""

            # Generate response
            if sender_user_name != '' and model_output != '':
                my_bot_response = f'@{sender_user_name} {model_output}'
                twitter.reply_message_to(my_bot_response, sender_tweet_id)

    print('Shutting Down NLTK Twitter Bot')

main()
