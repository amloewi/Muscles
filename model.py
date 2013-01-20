import web
import datetime

log = web.database(dbn='sqlite', db="log")
#log = web.database(dbn='postgres', user='alexloewi', pw='dian4nao3', db='postgres')

def new_person(name, email):
	log.insert('person', name=name, email=email)

def record_workout(name, exercises):
	#Assumes 'person' already exists, forcing profile creation to be somewhere else, i.e. separate and simple.
	#log.insert('type') gets the id of the last inserted 'type'; the logic (such as it is) is that 'insert' always returns the id of the thing it inserted most recently, so when you insert with nothing, it returns the LAST id again, instead of a new one.
	#I'm using a feature where IDs are auto-generated (this happens simply by not putting them explicitly in the schema) but I need to access them to make the workout_exercise, hence the trick above
	# **x unpacks the DICTIONARY x into the arguments for a function. So, if f() expects f(arg1=a, arg2=2), and you have a dict d = {'arg1':x, 'arg2':y} you can throw it right into the function, using f(**d)
	#I do e['tablename'] because you can't do insert('workout', e**) --- I put ALL the args in the dict.
	#And I didn't intersperse the code with these massive notes because they were making it hard to read.
	
	#Sometimes, things are stupid: the {'name':name} dict here is where the $name in 'where' is getting its value. because 'name=Alex' doesn't work.
	
	
	# I MIGHT NEED TO BE MUCH MORE CAREFUL IN ... ASSUMING THESE EXIST, BEFORE I EXTRACT THEM? Or perhaps not --- everythin looks okay, except there should be a 'new user' feature, in general.
	
	#THERE MUST BE A BETTER WAY. But maybe there isn't.
	d = datetime.datetime.now().timetuple()[:6] #1) Get the date 2) make it a list of (year, month, etc.) 3) only take the parts want.
	d = [str(i) for i in d] #Turn the list of numbers into a list of strings
	date = d[0]+"-"+d[1]+"-"+d[2]+" "+d[3]+":"+d[4]+":"+d[5] #stick the strings together with the necessary date syntax: "y-m-d h:m:s"
	
	p = log.select('person', {'name':name}, where='name=$name')
	log.insert('workout', date=date, person_id=name)
	wid = log.insert('workout')
	log.insert('person_workout', name=p[0].name, workout_id=wid, date=date)
	
	for e in exercises:
		e['tablename'] = 'exercise'
		e['workout_id'] = wid
		log.insert(**e)
		eid = log.insert('exercise')
		log.insert('workout_exercise', workout_id=wid, exercise_id=eid)


def last_exercises(name):
	#Gets the most recent person_workout, i.e. workout for the given person
	pw = log.select('person_workout',
					{'name':name},
					where="name=$name",
					order='ROWID DESC',
					limit=1)
					
	#db.select calls return ITERATORS: this means that each time you access something IN them, that item is REMOVED. This is why it's important to cast them as lists immediately --- otherwise, checking to see if the	first element is THERE, and THEN trying to take it out, will result in it not being there when you actually try to remove it.		
	if pw:
		#There are ANY workouts,
		pw = list(pw)[0]
	else:
		return []
		
	#Make sure the workout has been done in the last x days --- otherwise, return nothing.
	#Also, dates in general just suck. This was done completely while reading from the python datetime module documentation.
	#wd = log.select('workout', {'workout_id:',pw.workout_id}, where="workout_id=$workout_id")
	#date = wd[0].date
	then = datetime.datetime.strptime(pw.date, "%Y-%m-%d %H:%M:%S")
	now = datetime.datetime.now()
	if (now - then).days < 3:
		pass
	else:
		return []	
		
	#If it's fresh, get the exercises for that workout. (I'm assuming there will always be SOME --- otherwise it's not a workout --- but that's not check explicitly.)
	exs = log.select('exercise', 
					{'workout_id':pw.workout_id}, 
					where="workout_id=$workout_id")
						
	return list(exs)



def get_person(name):
	return log.select('person', {'name':name}, where="name=$name")[0]

#def get_last_workout(ID, name):
#	return log.select('workout', where=)

def worked_out_recently(name):
	#Shit. Whatever. Not right now. Don't wanna fuck with dates and things.
	pass
# START PRINTING THINGS OUT

#I WANT: person.workout.exercises


def all_people():
	return log.select('person', order='ROWID')

def all_workouts():
	return log.select('workout', order='ID')

def all_exercises():
    return log.select('exercise', order='ID')

def all_person_workouts():
	return log.select('person_workout', order='ID')

def all_workout_exercises():
	return log.select('workout_exercise', order='ID')





#THESE DON'T MAKE SENSE NOW ... if the ids are automatic?
def delete_exercise(ID):
	#Find all the associated workouts, too
    log.delete('exercise', where="id=$id", vars=locals())

def delete_workout(ID):
	#Find all the associated exercises, too
    log.delete('workout', where="id=$id", vars=locals())
