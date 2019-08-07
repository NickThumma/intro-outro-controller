from global_settings import SETTINGS
from datetime import date
from random import shuffle
import requests
import json

class Jibo_Interactions(object):
	def __init__(self, user_info, jibo_info):
		#self.jibo = JiboCommand()  #will be from jibo_commands.py
		anim_file = open(SETTINGS.ANIM_FILENAME)
		self.anim_dict = json.loads(anim_file.read())
		for a in self.anim_dict:
			if a != 'intro' and type(self.anim_dict[a]) == list:
				shuffle(self.anim_dict[a])

		self.calendar = SETTINGS.SCHOOL_CALENDAR

		self.user_info = user_info #eventually replace with get request
		self.jibo_info = jibo_info #eventually either read request or part of settings
		self.session_history = [] #session names ordered from oldest to newest
		self.update_session_history()

	def update_session_history(self):
		if 'session' not in self.user_info:
			return
		#ordered from oldest to newest
		session_history = [session_name for session_name in self.user_info['session']]
		session_history.sort(key=lambda x: self.user_info['session'][x]['number'])
		self.session_history = session_history

	def get_opening_name(self):

		#first session - will either not have session field or empty session field unsure
		if 'session' not in self.user_info:
			return 'intro'
		if len(self.user_info['session']) == 0:
			return 'intro'

		#birthday - will DOB be included in user_info?
		current_date = date.today()
		if int(self.user_info['DOB'][:2]) == current_date.month and int(self.user_info['DOB'][3:5]) == current_date.day:
			return 'birthday_opening'
		#leap day birthday
		elif self.user_info['DOB'][:5] == '02/29' and (current_date.month, current_date.day) == (2, 28):
			return 'birthday_opening'

		#get most recent session
		last_session_string = self.user_info['session'][self.session_history[-1]]['date']
		last_session_date = date(int(last_session_string[6:]), int(last_session_string[:2]), int(last_session_string[3:5]))

		#vacation - need to determine what date range to try
		test_date = last_session_date
		holidays = set()
		while test_date != current_date:
			if self.calendar.get(test_date):
				holidays.add(self.calendar.get(test_date))
			try:
				test_date = test_date.replace(day=test_date.day+1)
			except:
				if test_date.month != 12:
					test_date = test_date.replace(day=1, month=test_date.month+1)
				else:
					test_date = test_date.replace(day=1, month=1, year=test_date.year+1)

		if len(holidays) != 0:
			print("Holidays are:", holidays)
			return 'vacation_opening' #need to figure out how to get specific holidays
									  #maybe change calendar to directly list opening names?

		#missed session
		if int(str(current_date - last_session_date).split(' ')[0]) > SETTINGS.MISSED_DAYS_THRESHOLD: #need to decide how many days need to be missed for this condition
			return 'missed_session_opening'

		#default: state or generic
		openings = ['opening_'+self.jibo_info['state'], 'opening']
		shuffle(openings)
		return openings[0]


	def do_intro(self):
		self.update_session_history()

		#get opening category to use
		opening = self.get_opening_name()
		
		if opening == 'intro':
			for anim_name in self.anim_dict['intro']:
				print(self.anim_dict[anim_name]) 
				#replace above with self.ros.send_jibo_command(JiboStorybookBehaviors.SPEAK, self.anim_dict[anim_name])
			return

		else:
			#get opening from category
			anim_name = self.anim_dict[opening][0]
			print(self.anim_dict[anim_name])
			#replace above with self.ros.send_jibo_command(JiboStorybookBehaviors.SPEAK, self.anim_dict[anim_name])
			shuffle(self.anim_dict[opening])
		
		#get # sessions since last chat
		num_sessions = 0
		for session_name in reversed(self.session_history):
			if 'chit_chat' in self.user_info['session'][session_name]:
				break
			num_sessions += 1

		#determine if there should be chat
		if num_sessions >= SETTINGS.SESSIONS_PER_CHAT:
			print("Chit chat")
			#replace above with the chat function

			#get enter category to use
			enters = ['enter_'+self.jibo_info['state'], 'enter']
			shuffle(enters)

			#get enter from category
			anim_name = self.anim_dict[enters[0]]
			print(self.anim_dict[anim_name])
			#replace above with self.ros.send_jibo_command(JiboStorybookBehaviors.SPEAK, self.anim_dict[anim_name])
			shuffle(self.anim_dict[enters[0]])

		else:
			#get enter from state category
			anim_name = self.anim_dict['enter_'+self.jibo_info['state']][0]
			print(self.anim_dict[anim_name])
			#replace above with self.ros.send_jibo_command(JiboStorybookBehaviors.SPEAK, self.anim_dict[anim_name])
			shuffle(self.anim_dict['enter_'+self.jibo_info['state']])


	def do_outro(self):
		#apply session-based decay here

		#last session, need a better way to determine if it's the last session
		if len(self.user_info['session']) == SETTINGS.MAX_SESSIONS - 1:
			print(self.anim_dict['winter_break_exit_01']) 
			#replace above with self.ros.send_jibo_command(JiboStorybookBehaviors.SPEAK, self.anim_dict[winter_break_exit_01'])
		
		#get exit from state category
		else:
			anim_name = self.anim_dict['exit_'+self.jibo_info['state']][0]
			print(self.anim_dict[anim_name])
			#replace above with self.ros.send_jibo_command(JiboStorybookBehaviors.SPEAK, self.anim_dict[anim_name])
			shuffle(self.anim_dict['exit_'+self.jibo_info['state']])

			#get closing
			anim_name = self.anim_dict['closing'][0]
			print(self.anim_dict[anim_name])
			#replace above with self.ros.send_jibo_command(JiboStorybookBehaviors.SPEAK, self.anim_dict[anim_name])
			shuffle(self.anim_dict['closing'])



#unsure if this class is necessary or if it'll be taken care of elsewhere
class Decay(object):
	def __init__(self, hourly_decay, session_decay, gain):
		self.hourly_decay = hourly_decay
		self.session_decay = session_decay
		self.gain = gain

	def do_hourly_decay(self, attributes): #need to figure out how to schedule
		attributes[1] -= self.hourly_decay
		attributes[2] -= .5*self.hourly_decay
		return attributes

	def do_session_decay(self, attributes):
		attributes[0] -= self.session_decay
		attributes[2] -= .5*self.session_decay
		return attributes

	def update_decay_rates(self, yesterday): #yesterday is stats in the form of [[energy, mood, curiosity], ...]
		avg_attributes = [sum(yesterday[i][j] for i in range(len(yesterday)))/len(yesterday) for j in range(3)]
		
		if sum(avg_attributes)/3 < 4:
			self.hourly_decay -= self.gain*self.hourly_decay
			self.session_decay -= self.gain*self.session_decay
		
		elif sum(avg_attributes)/3 > 6:
			self.hourly_decay += self.gain*self.hourly_decay
			self.session_decay += self.gain*self.session_decay
		
		else:
			pass



















