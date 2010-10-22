import os
from google.appengine.ext.webapp import template

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import helpers

class RssHandler(webapp.RequestHandler):
  def get(self):
    page_id = 1
    page_items = 10
    
    blog_id = '31652320'
    
    blogger = helpers.Blogger(blog_id)
    blog = blogger.get_feeds(page_id, page_items)
    template_values = {
      'blog': blog
    }
    
    path = os.path.join(os.path.dirname(__file__), 'rss.xml')
    
    self.response.headers['Content-Type'] = 'text/xml'
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/rss.xml', RssHandler)], debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()

