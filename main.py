from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util, template
from google.appengine.api import mail

def sendMailWithStory(to,story,storyBit):
    mail.send_mail(sender="TeamStory <santiago1717@gmail.com>",
              to=to,
              subject="New Story Bit, its your turn",
              body="""
Dear TeamStory Player:

Story: %(title)s
Author: %(author1Nick)s and %(author2Nick)s
Last bit of the story:
%(storyBit)s

Your friend just wrote the next part of the story, its your time, to read it and write your part please click on the next link:
http://teamstories.appspot.com/storybit/%(KEY)s

Cheers

The TeamStory Team
""" % {'title' : story.title, "author1Nick" :  story.author1Nick, "author2Nick" : story.author2Nick, "storyBit" : storyBit.text, "KEY" : storyBit.key()})

class Story(db.Model):
    author1 = db.StringProperty(required=True)
    author1Nick = db.StringProperty(required=True)
    author2 = db.StringProperty(required=True)
    author2Nick = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    when = db.DateTimeProperty(auto_now_add=True)
 
class StoryBit(db.Model):
    story = db.ReferenceProperty(Story)
    text = db.StringProperty(required=True, multiline=True)
    author = db.StringProperty(required=True)
    authorNick = db.StringProperty(required=True)
    linkKey = db.StringProperty()
    when = db.DateTimeProperty(auto_now_add=True)

class MainHandler(webapp.RequestHandler):
    def get(self):
        stories = Story.all()
        self.response.out.write(template.render('templates/main.html', locals()))

class StoryBitHandler(webapp.RequestHandler):
    def get(self,key):
        storyBitBefore = StoryBit.get(key);
        storyBitNow = StoryBit.all().filter("linkKey =", key).fetch(1)
        if(storyBitBefore and not storyBitNow):
            storyBits = StoryBit.all().filter("story =", storyBitBefore.story).order("when")
            enableForm = True
            story = storyBitBefore.story
            self.response.out.write(template.render('templates/story.html', locals()))
        else:
            self.redirect("/")

    def post(self,key):
        storyBitBefore = StoryBit.get(key)
        storyBitNow = StoryBit.all().filter("linkKey =", key).fetch(1)
        if(storyBitBefore and not storyBitNow):
           author = storyBitBefore.author
           authorNick = storyBitBefore.authorNick
           if(author == storyBitBefore.story.author1):
               author = storyBitBefore.story.author2
               authorNick = storyBitBefore.story.author2Nick
           else:
               author = storyBitBefore.story.author1
               authorNick = storyBitBefore.story.author1Nick
           storyBitNow = StoryBit(story=storyBitBefore.story,authorNick=authorNick,author=author,linkKey=key,text=self.request.get("byte"))
           storyBitNow.put()
           sendMailWithStory(storyBitBefore.author,storyBitBefore.story,storyBitNow)
           self.redirect("/story/" + str(storyBitBefore.story.key()))
        else:
           self.redirect("/")

class NewHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('templates/new.html', locals()))
    def post(self):
       story = Story(author1=self.request.get("player1"), 
                     author1Nick=self.request.get("player1Nick"), 
                     author2=self.request.get("player2"), 
                     author2Nick=self.request.get("player2Nick"), 
                     title=self.request.get("title"))
       story.put()
       storyBit = StoryBit(author=self.request.get("player1"), story=story, authorNick=self.request.get("player1Nick"), text=self.request.get("byte")) 
       storyBit.put()
       sendMailWithStory(self.request.get("player2"),story,storyBit)
       #TODO: Send a mail to the author2 telling him to rock
       self.redirect('/')

class StoryHandler(webapp.RequestHandler):
    def get(self,key):
        story = Story.get(key)
        storyBits = StoryBit.all().filter("story =", story).order("when")
        self.response.out.write(template.render('templates/story.html', locals()))

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/new', NewHandler),
                                          ('/story/(.+)', StoryHandler),
                                          ('/storybit/(.+)', StoryBitHandler),
                                         ], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
