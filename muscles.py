import web
import model
import json

urls = (
	'/',	 		'welcome',
	'/index', 		'index',
	'/gaze', 		'gaze',
	'/gaze/(.*)', 	'show_person',
	'/record',		'record',
	'/record/(.*)',	'enter_workout',
	'/success',		'success',
	'/empty',		'empty',
	'/new_user', 	'new_user',
)

render = web.template.render('templates')

class welcome:
	#Welcome! Would you like to gaze, or record?
	def GET(self):
		return render.welcome()
		
class gaze:
	#At who would you like to gaze?
	def GET(self):
		ppl = list(model.all_people())
		return render.list_users(ppl, 'gaze')
		
class show_person:
	#Here is the last workout of the person you want to gaze at,
	# IFF it was performed within the last three days. (It says TWO days
	# on the site so that you won't get annoyed when you exercise ON
	# THE THIRD DAY and still get harangued.)
	def GET(self, person):
		exs = list(model.last_exercises(person))
		return render.show_person(exs)
		
class record:
	#Who are you, so that you can record a workout for yourself?
	def GET(self):
		ppl = list(model.all_people())
		return render.list_users(ppl, 'record')
	
	
	
class enter_workout:
	
	def GET(self, person):
		#'person' is the NAME in /record/name. 
		return render.record_workout(person)

	def POST(self, person):
		#However HERE, 'person' is the WHOLE string 'record/name'
		# ALL DEPENDS on whether you say the url is "a/b" or "/a/b"
		workout = web.data()
		if workout:
			workout = json.loads(workout)
			#print 'WORKOUT: ', workout
			exs = []
			for ex in workout['exercises']:
				exs.append({e['name']: e['value'] for e in ex})
			workout['exercises'] = exs
			
			model.record_workout(**workout)#name, date, exercises)
		else:
			render.empty()
		
		
		# THIS doesn't actually ... render the page, as I expected. I have to use window.location = .
		#return web.seeother('/success')

		
class success:
	def GET(self):
		return render.success()
		
class empty:
	def GET(self):
		return render.empty()

class new_user:
	def GET(self):
		return render.new_user()
		
	def POST(self):
		info = web.data()
		if info:
			info = json.loads(info)
			#print info
			info = {i['name']:i['value'] for i in info}
			model.new_person(**info)


app = web.application(urls, globals()) #what's in globals?

if __name__ == "__main__":	
	
	# If I just deleted the database,
	# (which I do periodically as part of testing)
	# I want to make sure we're in it
	if len(list(model.all_people())):
		#i.e. is length is NOT 0 (i.e. False), don't do anything.
			pass
	else:
		model.new_person(name='Shelly', email='ms.knee@gmail.com')
		model.new_person(name='Alex', email='amloewi@gmail.com')
		
	
	w = {
		'name':'Alex',
		#'date':"2012-01-16 12:25:34", #Now generated automatically in record_workout
		'exercises':[
						{
						 'muscle':'butt',
						 'sets':3,
						 'reps':10,
						 'weight':125
						 },
						
						 {
						 'muscle':'pecs',
						 'sets':3,
						 'reps':10,
						 'weight':125
						 },
					]
	}
	
	#model.record_workout(**w)
	#w['name'] = 'Shelly'
	#w['date'] = "2013-01-15 12:25:34"
	#model.record_workout(**w)
	app.run()
	
	