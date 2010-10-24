import os
from google.appengine.ext.webapp import template

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from recaptcha.client import captcha

#import helpers
from helpers import *

class MainHandler(webapp.RequestHandler):
  def post(self):
    path = self.request.path.split('/')
    remoteip = self.request.remote_addr
    url = self.request.url
    
    name = self.request.get('name')
    email = self.request.get('email')
    comment = self.request.get('comment')
    challenge = self.request.get('recaptcha_challenge_field')
    response  = self.request.get('recaptcha_response_field')
    post_id = long(path[2])
    
    cResponse = captcha.submit(challenge, response, '6LdOAb4SAAAAALH1zbcxUkjwFYJQItNFHDd5zj_h', remoteip)

    if cResponse.is_valid:
      comment = BlogComment(
        post_id = post_id,
        name = name,
        email = email,
        comment = comment)
      comment.put()
      
      self.redirect(url)
    else:
      error = 'The values were not valid.'
      self.response.out.write('It failed with error code: ' + error);
  
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
    
    chtml = captcha.displayhtml(
      public_key = "6LdOAb4SAAAAAEkajiU_r5ksvtPasK7EUAXKKtnD",
      use_ssl = False,
      error = None)
      
    template_values = { 
      'captchahtml': chtml,
      'tweets': tweets,
      'blog': blog
    }
    
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/', MainHandler), ('/post/.*', MainHandler), ('/page/.*', MainHandler)], debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
