import tweepy, os, emoji
from spellchecker import SpellChecker
from dotenv import load_dotenv
load_dotenv()

class Tweeter:
	def __init__(self, api_key, api_secret, access_token, access_secret):
		auth = tweepy.OAuthHandler(api_key, api_secret)
		auth.set_access_token(access_token, access_secret)
		self.api = tweepy.API(auth)
		# Can be changed to any other users
		self.own = "geileytypos"
		self.target = "bendover1312"
		self.checker = SpellChecker(language='de',case_sensitive=False)
  
	def tweet(self, text):
		self.api.update_status(text)
  
	def getLatestRetweet(self):
		"""Returns the latest retweet of the account under self.own, is used for only searching part of the timeline
		"""
		me = self.api.get_user(screen_name=self.own)
		timeline = me.timeline()
		for tweet in timeline:
			if tweet.text.startswith("RT"):
				return tweet
		return None
	
	def containsError(self, tweet):
		"""Filters out all mentions and retweet hints and runs the spellchecker

		Args:
			tweet: The tweet object

		Returns:
			boolean: indicates error
		"""
		mentions = tweet.entities['user_mentions']
		display_names = ['@' + mention['screen_name'] for mention in mentions]
		tweet_text = tweet.text.replace("RT", "").replace(":","")
		for name in display_names:
			tweet_text = tweet_text.replace(name, "")
		tweet_text = tweet_text.strip().split(" ")
		errors = self.checker.unknown(tweet_text)
		false_positives = 0
		for error in errors:
			if (error == self.checker.correction(error)) or self.containsEmoji(error):
				false_positives += 1
		return (len(errors) - false_positives) != 0

	def containsEmoji(self, text):
		for word in text:
			if emoji.is_emoji(word):
				return True
		return False
	
	def search_timeline(self):
		latest = self.getLatestRetweet()
		timeline = self.api.get_user(screen_name=self.target).timeline()
		for tweet in timeline:
			if tweet.id == latest.retweeted_status.id:
				break
			if self.containsError(tweet):
				#tweet.retweet()
				pass


this = Tweeter(os.getenv("API_KEY"), os.getenv("API_SECRET"), os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_SECRET"))
this.search_timeline()