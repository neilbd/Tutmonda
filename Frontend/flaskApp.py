from pymongo import MongoClient
from flask import Flask, render_template, send_file
import json
app = Flask(__name__)

client = MongoClient()
print app.config["SERVER_NAME"]
print "CLIENT"
print client

db = client.main

print db

@app.route("/", methods=['GET'])
def start():
	print "HERE"

	try:
		return app.send_static_file('index.html')
	except Exception as error:
		print error

@app.route("/spiders", methods=['GET'])
def getSpiders():
	print "GOT SPIDERS"
	store = []
	obj = {}
	for spider in db.spiders.find():
		print spider
		change = spider.keys()
		for key in change:
			print key
			if key != '_id':
				if type(spider[key]) is unicode:
					val = spider[key].encode('ascii','ignore')
				else:
					val = spider[key]
				print type(key.encode('ascii','ignore'))
				obj[key.encode('ascii','ignore')] = val
		print obj
		store.append(obj)
		print "Appended"
		obj = {}

	print "FINISHED"

	print json.dumps(store)
	
	return (json.dumps(store), 200, {'Accept': 'application/json', 'Access-Control-Allow-Origin': '*'})

if __name__ == "__main__":
	app.run()
