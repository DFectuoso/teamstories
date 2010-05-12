import unittest
import ts_test_framework
from example_module import ExampleModule

class ExampleModuleTest(ts_test_framework.TeamStoriesTest):
	def setUp(self):
		self.em = ExampleModule()
		
	def test_identityReturnsInts(self):
		self.assertEqual(1, self.em.identity(1))
		
	def test_identifyDoesntModifyInts(self):
		self.assertNotEqual(3, self.em.identity(4))

		
if __name__ == '__main__':
    unittest.main()