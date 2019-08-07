from Georgia_Intro_Outro import Jibo_Interactions
from datetime import date

#user specific info, template
user =  {'info': {'assessment': {}, 
				  'condition': '', 
				  'session': {'01': {'activity': {'end_time': '83464', 
				  													'start_time': '98734', 
				  													'type': 'storybook'}, 
													   #'chit_chat': {'question': "what's your favorite color?", 
													   #				 'response': 'blue'}, 
													   'date': '07/08/2019', 
													   'end_time': '874875759', 
													   'interrupt': {'number': 0, 
													   				 'reason': 'things went wrong'}, 
													   'number': 0, 
													   'robotID': 3, 
													   'robot_post_state': 'LLL', 
													   'robot_pre_state': 'HHL', 
													   'start_time': '98878897'},

							  '02': {'date': '06/08/2019', 
							  						   'end_time': '874875759', 
							  						   'interrupt': {'number': 0, 
							  						   				 'reason': 'things went wrong'}, 
							  						   'number': 1, 
							  						   'start_time': '98878897'},
							  '03': {'date': '05/08/2019', 
							  						   'end_time': '874875759', 
							  						   'interrupt': {'number': 0, 
							  						   				 'reason': 'things went wrong'}, 
							  						   'number': 2, 
							  						   'start_time': '98878897'}
							  }, 
				  'word_list': ['abc', 'def'],
				  'DOB': '01/30/1998'
				 },
		 'subject_id': 'p002'
		}

#jibo specific info
jibo_info = {'jibo_id':'01',
			 'state':'HHH',
			 'decay_rates': {'hourly_decay': .1,
			 				 'session_decay': .3,
			 				 'gain':.1
			 				},
			 'attributes': {}
			}

jibo_info['attributes']['attr_001'] =  {'timestamp': '1564516000', #is the database using unix time?
			 							'energy': '5.0',
			 							'mood': '5.0',
			 							'curiosity': '5.0'}


################################################################################
#									INTROS									   #
################################################################################
#test intro

#no session field
print("\nno_session_intro_test:")
no_session_user =  {'info': {'assessment': {}, 
							 'condition': '', 
							 'word_list': [],
							 'DOB': '01/30/1998'
							},
					'subject_id': 'p001'
				   }

no_session_test = Jibo_Interactions(no_session_user['info'], jibo_info)
no_session_test.do_intro()

#empty session field
print("\nempty_session_intro_test:")
empty_session_user = {'info': {'assessment': {}, 
							   'condition': '', 
							   'word_list': [],
							   'DOB': '01/30/1998',
							   'session': {}
							  },
					  'subject_id': 'p001'
					 }

empty_session_test = Jibo_Interactions(empty_session_user['info'], jibo_info)
empty_session_test.do_intro()

################################################################################
#test birthday

#standard birthday
print("\nbirthday_intro_test:")
birthday_user = {'info': {'assessment': {}, 
						  'condition': '', 
						  'word_list': [],
						  'DOB': str(date.today())[5:7]+'/'+str(date.today())[8:]+'/1998',
						  'session': {
						  			  '01': {'date': '06/08/2019',
						  			  		 'number': 1
						  			  		},
							  		  '02': {'date': '05/08/2019',
							  		  		 'number': 2
							  				}
						  			 }
						 },
				 'subject_id': 'p001'
				}

birthday_test = Jibo_Interactions(birthday_user['info'], jibo_info)
birthday_test.do_intro()

#TODO: leap day birthday

################################################################################
#test vacation (w/ school_calendar) / test missed days (with empty_calendar) since vacation days take priority
print('\nvacation_intro_test')
vacation_user = {'info': {'assessment': {}, 
						  'condition': '', 
						  'word_list': [],
						  'DOB': '01/30/1998',
						  'session': {
						  			  '01': {'date': '06/08/2019',
						  			  		 'number': 1
						  			  		},
							  		  '02': {'date': '05/08/2019',
							  		  		 'number': 2
							  				}
						  			 }
						 },
				 'subject_id': 'p001'
				}

vacation_test = Jibo_Interactions(vacation_user['info'], jibo_info)
vacation_test.do_intro()

################################################################################
#test default
#need to switch calendar to test since vacation takes priority

print('\ndefault_intro_test')
default_user =  {'info': {'assessment': {}, 
						  'condition': '', 
						  'word_list': [],
						  'DOB': '01/30/1998',
						  'session': {
						  			  '01': {'date': '05/08/2019',
						  			  		 'number': 1
						  			  		},
							  		  '02': {'date': '08/06/2019',
							  		  		 'number': 2
							  				}
						  			 }
						 },
				 'subject_id': 'p001'
				}

default_test = Jibo_Interactions(default_user['info'], jibo_info)
default_test.do_intro()


################################################################################
#									OUTROS									   #
################################################################################
#test last outro
print('\nlast_outro_test')
last_user = {'info': {'assessment': {}, 
					  'condition': '', 
					  'word_list': [],
					  'DOB': '01/30/1998',
					  'session': {}
					 },
			 'subject_id': 'p001'
			}

for i in range(44):
	last_user['info']['session'][str(i)] = {'date': '01/01/2019', 'number': i}
last_outro_test = Jibo_Interactions(last_user['info'], jibo_info)
last_outro_test.do_outro()

################################################################################
#test default outro

print('\ndefault_outro_test')
default_user =  {'info': {'assessment': {}, 
						  'condition': '', 
						  'word_list': [],
						  'DOB': '01/30/1998',
						  'session': {
						  			  '01': {'date': '05/08/2019',
						  			  		 'number': 1
						  			  		},
							  		  '02': {'date': '08/06/2019',
							  		  		 'number': 2
							  				}
						  			 }
						 },
				 'subject_id': 'p001'
				}
default_outro_test = Jibo_Interactions(default_user['info'], jibo_info)
default_outro_test.do_outro()