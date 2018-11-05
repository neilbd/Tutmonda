
from pymongo import MongoClient
import requests
import json

client = MongoClient()

print "CLIENT"
print client

db = client.main

print db

class SpiderCollection:
	
	# Activates the crawling process for spiders stored in the database

	db_use = db

	@staticmethod
	def run(topic):
		results = []
		url = 'https://gateway-a.watsonplatform.net/calls/data/GetNews?outputMode=json&start=now-30d&end=now&count=5&q.enriched.url.enrichedTitle.keywords.keyword.text=' + topic.replace(" ", "%20") + '&return=enriched.url.url,enriched.url.title&apikey='
		r = requests.get(url)
		print r.text

		if r.json()['status'] == 'ERROR':
			print "ERROR for " + topic + ", no URL's collected"
			return
		else:
			for element in r.json()['result']['docs']:
				title = element['source']['enriched']['url']['title'].replace(u"\u2019", "\'")
				results.append([title, element['source']['enriched']['url']['url']])
			spider_to_replace = db.spiders.find_one({'name': topic})
			db.spiders.find_one_and_replace({'name': topic}, {'name': topic, 'links': results, 'assigned_column': spider_to_replace['assigned_column']})


	@staticmethod
	def runSpiders():

		string = ""

		spiders = db.spiders.find({'name': {"$exists": True}})

		for spider in spiders:
			print spider
			SpiderCollection.run(spider['name'])

		spiders = db.spiders.find()

	@staticmethod
	def addSpider(topic):

		if db.spiders.find_one({"name": topic}) != None:
			print "Already a topic!"
			return

		if db.spiders.find_one({'column': 1}) == None:
			db.spiders.insert({'column': 1, 'count': 1})
			db.spiders.insert({'name': topic, 'links': None, 'assigned_column': 1})

		elif db.spiders.find_one({'column': 2}) == None:
			db.spiders.insert({'column': 2, 'count': 1})
			db.spiders.insert({'name': topic, 'links': None, 'assigned_column': 2})

		else:

			count_one = db.spiders.find_one({'column': 1})['count']
			count_two = db.spiders.find_one({'column': 2})['count']

			if count_one <= count_two:
				db.spiders.insert({'name': topic, 'links': None, 'assigned_column': 1})
				db.spiders.find_one_and_replace({'column': 1}, {'column': 1, 'count': count_one+1})
			else:
				db.spiders.insert({'name': topic, 'links': None, 'assigned_column': 2})
				db.spiders.find_one_and_replace({'column': 2}, {'column': 2, 'count': count_two+1})

	@staticmethod
	def removeSpider(name):

		spider = db.spiders.find_one({'name': name})
		count = db.spiders.find_one({'column': spider["assigned_column"]})['count']
		db.spiders.find_one_and_replace({'column': spider["assigned_column"]}, {'column': spider["assigned_column"], 'count': count-1})
		db.spiders.delete_one({'name': name})
		
