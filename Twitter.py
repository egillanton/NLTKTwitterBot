from TwitterAPI import TwitterAPI


def get_api():
    # TODO: Remove for public release
    consumer_key = 'gOyKYCNXZhOEzuXCCniFYLqVi'
    consumer_secret = 'rKF7W6gxbt9ArjIrrCRvDwxUBQrRROAvRl5hDHm7cAnOpOcWo6'
    access_token_key = '1051128664631517185-FQhAHJo6WixffqbgIYjXUzYM6YFwO9'
    access_token_secret = 'hUE0TTAdYclgbhPcUxwpPINx326VzCgaqmQf8PMk0s3Ys'
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
    return api
