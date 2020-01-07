from tweepy import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import unidecode
import time
from threading import Thread
import sys
from matplotlib import pyplot as plt

class UI:
	def __init__(self):
		self.ERASE_LINE = '\x1b[2K'
		self.running = True
	
	def terminate(self):
		self.running = False
		sys.stdout.write(self.ERASE_LINE)
	
	def fetching_ui(self):
		while self.running:
			for i in range(5):
				print('Fetching tweets'+('.'*i), end='\r')
				time.sleep(1)
			sys.stdout.write(self.ERASE_LINE)
		print()

	def analysing_ui(self):
		self.running = True
		sprint = ['/','-','\\','|']
		while self.running:
			for i in range(len(sprint)):
				print('Analysing tweets '+sprint[i], end='\r')
				time.sleep(0.2)
		sys.stdout.write(self.ERASE_LINE)
		print()

consumerKey = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
consumerSecret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
accessToken = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
accessTokenSecret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

query = input('Enter keyword or query: ')
num = int(input('No. of entries: '))

auth = OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = API(auth)

ui = UI()
c = Thread(target=ui.fetching_ui)
c.start()
tweets = Cursor(api.search, q=query, lang='en').items(num)
ui.terminate()

c.join()
c = Thread(target=ui.analysing_ui)
c.start()
analyzer = SentimentIntensityAnalyzer()

pos = 0
neg = 0
neu = 0

for x in tweets:
	polarity = analyzer.polarity_scores(unidecode.unidecode(x.text))
	
	if polarity['compound'] < 0:
		neg += 1
	elif polarity['compound'] > 0.0:
		pos += 1
	else:
		neu += 1
ui.terminate()
c.join()

neg = neg*100/num
neu = neu*100/num
pos = pos*100/num

print('Result:')
print('Neg: {:.2f}%'.format(neg), end='\t')
print('Neu: {:.2f}%'.format(neu), end='\t')
print('Pos: {:.2f}%'.format(pos), end='\t')
print()

sizes = [neg,neu,pos]
explode = [0.0,0.0,0.0]
explode[sizes.index(max(sizes))] = 0.1
clr = ['#A22A10','#455CAB','#359C36']
labels = ['Neg: {:.2f}%'.format(neg),'Neu: {:.2f}%'.format(neu),'Pos: {:.2f}%'.format(pos)]

plt.pie(sizes, labels=labels, explode=explode, colors=clr, shadow=True)
plt.show()
