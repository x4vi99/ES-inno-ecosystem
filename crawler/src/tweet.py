import json

class Tweet:
    def __init__(self, id, text, user, date, url,
                 hashtags, likes, retweets, terms):
        self.id = int(id)
        self.text = text
        self.user = int(user)
        self.date = date
        self.url = url
        self.hashtags = hashtags
        self.likes = likes
        self.retweets = retweets
        self.terms = terms

    def get_terms(self):
        return self.terms

    @staticmethod
    def from_json(json_str):
        tweet_json = json.loads(json_str)
        return Tweet(
            tweet_json['ID'], tweet_json['Tweet_text'], tweet_json['UserId'],
            tweet_json['Date'], tweet_json['URL'], tweet_json['Hashtags'],
            tweet_json['Likes'], tweet_json['Number_Retweets'], tweet_json['terms']
        )

    def to_json(self):
        return {
            'ID': self.id,
            'Tweet_text': self.text,
            'UserId': self.user,
            'Date': self.date,
            'URL': self.url,
            'Hashtags': self.hashtags,
            'Likes': self.likes,
            'Number_Retweets': self.retweets,
            'terms': self.terms
        }

    def __str__(self):
        return ('%s\n %s | %s | %s | %s | %s | %s' %
                (self.text, self.user, self.date, self.hashtags, self.likes, self.retweets, self.url))

    def row_data(self):
        return (self.text, self.user, self.date, self.hashtags, self.likes, self.retweets, self.url)