from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('templates/main.html', locals()))

class NewHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('templates/new.html', locals()))
    def post(self):
        #TODO: We need to save the information we get in the post right here
       self.redirect('/')

class StoryHandler(webapp.RequestHandler):
    def get(self,story_id):
        self.response.out.write(template.render('templates/story.html', locals()))

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/new', NewHandler),
                                          ('/story/(.+)', StoryHandler),
                                         ], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
