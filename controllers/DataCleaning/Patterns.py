import re

URL_PATTERN=re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
HASHTAG_PATTERN = re.compile(r'#\w*')
MENTION_PATTERN = re.compile(r'@\w*')
RESERVED_WORDS_PATTERN = re.compile(r'^(RT|FAV)')

try:
    # UCS-4
    EMOJIS_PATTERN = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
except re.error:
    # UCS-2
    EMOJIS_PATTERN = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')

SMILEYS_PATTERN = re.compile(r"(?:X|:|;|=)(?:-)?(?:\)|\(|O|D|P|S){1,}", re.IGNORECASE)
NUMBERS_PATTERN = re.compile(r"(^|\s)(\-?\d+(?:\.\d)*|\d+)")


def remove_from_tweet(tweet):
    tweet = URL_PATTERN.sub('', tweet)
    tweet = HASHTAG_PATTERN.sub('', tweet)
    tweet = RESERVED_WORDS_PATTERN.sub('', tweet)
    tweet = EMOJIS_PATTERN.sub('', tweet)
    tweet = SMILEYS_PATTERN.sub('', tweet)
    tweet = NUMBERS_PATTERN.sub('', tweet)


    return tweet

