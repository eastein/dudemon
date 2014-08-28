import unittest
import dudeutils

class DudemonTests(unittest.TestCase) :
	def test_whom(self) :
		state = {'jim' : {'s' : 10, 'e' : 20}, 'ken' : {'s' : 12, 'e' : 20}, 'smitty' : {'s' : 15, 'e' : 20}, 'sumdood' : {}}
		self.assertEquals(dudeutils.whom(state, 1, 10), "jim will be here in 9 seconds.")
		self.assertEquals(dudeutils.whom(state, 1, 12), "jim and ken will be here in 11 seconds.")
		self.assertEquals(dudeutils.whom(state, 12, 12), "jim and ken are here now.")
		self.assertEquals(dudeutils.whom(state, 1, 15), "jim, ken, and smitty will be here in 14 seconds.")
		self.assertEquals(dudeutils.whom(state, 1, 1), "nobody is here now.")
		self.assertEquals(dudeutils.whom(state, 1, 2), "nobody will be here in 1 second.")

	def test_when_upcoming(self) :
		state = {
			'alice' : {'s' : 5, 'e' : 10},
			'bob' : {'s' : 7, 'e' : 12}
		}

		self.assertEquals(dudeutils.when(state, 1, count=1), "alice will be here in 4 seconds.")
		self.assertEquals(dudeutils.when(state, 5, count=1), "alice will be here in a jiffy.")

	def test_when_past_and_future(self) :
		state = {
			'alice' : {'s' : 5, 'e' : 10},
			'bob' : {'s' : 7, 'e' : 12}
		}
		self.assertEquals(dudeutils.when(state, 8, count=2), "bob got here 1 second ago and alice will leave in 2 seconds.")

	def test_when_talk_about_each_person_once(self) :
		state = {
			'alice' : {'s' : 3, 'e' : 4},
			'bob' : {'s' : 8, 'e' : 12}
		}
		self.assertEquals(dudeutils.when(state, 5, count=2), "alice left 1 second ago and bob will be here in 3 seconds.")

	def test_when_ennui(self) :
		state = {}
		self.assertEquals(dudeutils.when(state, 3), "The only thing I know is that I know nothing.")

	def test_when_future_leaving(self) :
		state = {'jim' : {'s' : 5, 'e' : 10}}
		self.assertEquals(dudeutils.when(state, 8), "jim will leave in 2 seconds.")

	def test_when_past_leaving(self) :
		state = {'jim' : {'s' : 5L, 'e' : 10L}}
		self.assertEquals(dudeutils.when(state, 11), "jim left 1 second ago.")

	def test_when_unsetup_user(self) :
		state = {'jim' : {}}
		self.assertEquals(dudeutils.when(state, 5), "The only thing I know is that I know nothing.")

	def test_overlap(self) :
		state = {
		  'jim' : {'s' : 10, 'e' : 20},
		  'ken' : {'s' : 12, 'e' : 16},
		  'smitty' : {'s' : 15, 'e' : 20},
		  'sumdood' : {}
                }
		self.assertEquals(dudeutils.overlap(state, 25, 25), list())
		self.assertEquals(dudeutils.overlap(state, 0, 1), list())
		self.assertEquals(dudeutils.overlap(state, 0, 10), ['jim'])
		self.assertEquals(dudeutils.overlap(state, 0, 11), ['jim'])
		self.assertEquals(dudeutils.overlap(state, 0, 12), ['jim', 'ken'])

	def test_oxford(self) :
		self.assertEquals(dudeutils.oxford(['a']), 'a')
		self.assertEquals(dudeutils.oxford(['a', 'b']), 'a and b')
		self.assertEquals(dudeutils.oxford(['a', 'b', 'c']), 'a, b, and c')
