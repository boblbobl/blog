import os
from google.appengine.ext.webapp import template

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from recaptcha.client import captcha

import helpers

class MainHandler(webapp.RequestHandler):
  def post(self):
    
    challenge = self.request.get('recaptcha_challenge_field')
    response  = self.request.get('recaptcha_response_field')
    remoteip = self.request.remote_addr
    
    cResponse = captcha.submit(challenge, response, '6LdOAb4SAAAAALH1zbcxUkjwFYJQItNFHDd5zj_h', remoteip)
    
    
    
    if cResponse.is_valid:
      # response was valid
      # other stuff goes here
      self.response.out.write('It worked!' + challenge + ' ' + response);
    else:
      error = cResponse.error_code
      self.response.out.write('It failed with error code: ' + error);
  
  def get(self):
    twitter_id = '7942102'
  
    twitter = helpers.Twitter(twitter_id)
    tweets = twitter.get_feeds()
    
    path = self.request.path.split('/')
    action = path[1].lower()
    
    blog_id = '31652320'
    blogger = helpers.Blogger(blog_id)
    
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
