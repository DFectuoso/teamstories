import unittest
import ts_test_framework

class UrlTest(ts_test_framework.TeamStoriesTest):
	def setUp(self):
		pass
		
	def test_rootEmitsHelloWorld(self):
		self.web_get("") #empty string should map to http://localhost:8080/
		self.assertDocumentContains("Team Stories")
		
if __name__ == '__main__':
    unittest.main()