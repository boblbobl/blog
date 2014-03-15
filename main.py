import os
from google.appengine.ext.webapp import template

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from recaptcha.client import captcha

from helpers import *


class MainHandler(webapp.RequestHandler):  
  def get(self):
    twitter_id = '7942102'
  
    twitter = Twitter(twitter_id)
    tweets = twitter.get_feeds()
    
    path = self.request.path.split('/')
    action = path[1].lower()
    
    blog_id = '31652320'
    blogger = Blogger(blog_id)
    
    page_items = 10
    single_post = False
    
    if (action == 'post'):
      post_id = path[2]
      blog = blogger.get_post(post_id)
    elif (action == 'page'):
      page_id = int(path[2])
      blog = blogger.get_feeds(page_id, page_items)
    else:
      page_id = 1
      blog = blogger.get_feeds(page_id, page_items)
      
    template_values = {
      'blog': blog
    }
    
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/', MainHandler), ('/post/.*', MainHandler), ('/page/.*', MainHandler)], debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
