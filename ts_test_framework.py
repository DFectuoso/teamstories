import unittest
import urllib2

class TeamStoriesTest(unittest.TestCase):
	document = None
	document_string = None
	
	def assertContains(self, haystack, needle):
		self.assertTrue(needle in haystack)
		
	def web_get(self, url, data=None):
		full_url = "http://localhost:8080/"+url
		self.document = urllib2.urlopen(full_url, data)
		self.document_string = "".join(self.document)
		
	def assertDocumentContains(self, needle):
		if(None==self.document):
			raise Exception("You need to do a web hit before you can check document contents.  Try TeamStoriesTest.web_get()")
		self.assertTrue(needle in self.document_string)
		

	#in here we'll put methods that should be common across all test cases
	