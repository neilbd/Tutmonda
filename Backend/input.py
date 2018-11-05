from SpiderCollection import SpiderCollection

while True:
	
	try:
		choice = input("Press 1 to add a spider, 2 to remove a spider, 3 to view active spiders, or 0 to exit: ")

		if choice == 1:

			topic = input("What topic should the spider cover?: ")

			SpiderCollection().addSpider(topic)

			print topic + " spider added!\n"

		elif choice == 2:

			name = input("What spider would you like to remove?: ")

			SpiderCollection().removeSpider(name)

			print name + " spider removed!\n"

		elif choice == 3:

			spiders = SpiderCollection.db_use.spiders.find()
			for spider in spiders:
				print spider

		elif choice == 4:
			SpiderCollection().runSpiders()

		elif choice == 0:
			break

		else:
			continue
	except Exception:
		print "Format error for inserting data"
	
print "Thank you!"
