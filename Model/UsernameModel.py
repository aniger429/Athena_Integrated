
class UsernameModel(object):
    idUsername = -1
    username = ""
    numTweets = 0
    numMentions = 0

    def __init__(self, idUsername=-1, username="", numTweets=0, numMentions=0):
        self.idUsername = idUsername
        self.username = username
        self.numTweets = numTweets
        self.numMentions = numMentions
