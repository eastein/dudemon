import unittest
import dudeutils

class DudemonTests(unittest.TestCase) :
	def test_whom(self) :
		state = {'jim' : {'s' : 10, 'e' : 20}, 'ken' : {'s' : 12, 'e' : 20}, 'smitty' : {'s' : 15, 'e' : 20}}
		self.assertEquals(dudeutils.whom(state, 1, 10), "jim will be here in 9 seconds.")
		self.assertEquals(dudeutils.whom(state, 1, 12), "jim and ken will be here in 11 seconds.")
		self.assertEquals(dudeutils.whom(state, 1, 15), "jim, ken, and smitty will be here in 14 seconds.")
		self.assertEquals(dudeutils.whom(state, 1, 1), "nobody is here now.")
		self.assertEquals(dudeutils.whom(state, 1, 2), "nobody will be here in 1 second.")
