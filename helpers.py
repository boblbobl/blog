import os
import cgi
import hashlib

from gdata import service
import gdata
import atom

from dateutil import parser
from xml.dom import minidom

from google.appengine.api import urlfetch
from google.appengine.ext import db

class BlogComment(db.Model):
  post_id = db.IntegerProperty(required=True)
  name = db.StringProperty(required=True)
  email = db.StringProperty(required=True)
  comment = db.StringProperty(required=True)
  created = db.DateTimeProperty(auto_now=True)
  
class Twitter:
  def __init__(self, twitter_id):
    self.twitter_id = twitter_id
    
  def get_feeds(self):
    twitterfeed = urlfetch.fetch('http://twitter.com/statuses/user_timeline/' + self.twitter_id + '.xml?count=5')
    xml = minidom.parseString(twitterfeed.content)
    feeds = []
    for entry in xml.getElementsByTagName('status'):
      feeds.append({
        'published': parser.parse(entry.getElementsByTagName('created_at')[0].firstChild.data),
        'content': entry.getElementsByTagName('text')[0].firstChild.data
      })
      
    return feeds

class Blogger:
  def __init__(self, blog_id):
    self.blog_id = blog_id
    self.blogger_service = service.GDataService()
  
  def get_post(self, post_id):
    query = service.Query()
    query.feed = 'http://www.blogger.com/feeds/' + self.blog_id + '/posts/default/' + post_id
    entry = self.blogger_service.Get(query.ToUri())
    
    feeds = []
    feeds.append({
      'id': entry.id,
      'title': entry.title.text,
      'link': self.get_post_link(entry),
      'published': parser.parse(entry.published.text),
      'updated': entry.updated.text,
      'author': entry.author[0].name.text,
      'content': entry.content.text,
      'comments': self.get_comments(entry)
    })
    
    blog = {
      'page_id': -1,
      'post_id': post_id,
      'posts': feeds,
      'next_link': None,
      'prev_link': None,
      'singlepost': True
    }
    return blog
    
  def get_feeds(self, page_id, page_items):
    query = service.Query()
    query.feed = 'http://www.blogger.com/feeds/' + self.blog_id + '/posts/default'
    query.max_results = page_items
    query.start_index = ((page_id - 1) * page_items) + 1;
    
    feed = self.blogger_service.Get(query.ToUri())
    feeds = []
    for entry in feed.entry:
      feeds.append({
        'id': self.get_post_id(entry),
        'title': entry.title.text,
        'link': self.get_post_link(entry),
        'published': parser.parse(entry.published.text),
        'updated': entry.updated.text,
        'author': entry.author[0].name.text,
        'content': entry.content.text,
        'comments': self.get_comments(entry)
      })
      
    blog = {
      'page_id': page_id,
      'post_id': None,
      'posts': feeds,
      'next_link': self.get_next_link(page_id, feed),
      'prev_link': self.get_prev_link(page_id, feed),
      'singlepost': False
    }
    return blog
  
  def get_comments(self, entry):
    feeds = []
    q = BlogComment.gql('WHERE post_id = ' + str(self.get_post_id(entry)))
    
    for comment in q:
      feeds.append({
        'name': comment.name,
        'comment': comment.comment,
        'gravatar_link': self.get_gravatar_link(comment.email)
      })
      
    return feeds
    
  def get_gravatar_link(self, email):
    md5hash = hashlib.md5(email).hexdigest()
    return 'http://www.gravatar.com/avatar/' + md5hash + '?s=50&d=identicon'
 
  def get_next_link(self, page_id, feed):
    if (feed.GetNextLink() != None):
      return '/page/' + str(page_id + 1)
    else:
      return None
  
  def get_prev_link(self, page_id, feed):
    if (feed.GetPrevLink() != None):
      if page_id == 2:
        return '/'
      else:
        return '/page/' + str(page_id - 1)
    else:
      return None
  
  def get_post_id(self, entry):
    post_id = entry.id.text.replace('tag:blogger.com,1999:blog-31652320.post-', '')
    return long(post_id)
  
  def get_post_link(self, entry):
    post_id = self.get_post_id(entry)
    escaped_title = cgi.escape(entry.title.text.lower())
    #remove unnecessary chars
    link_title = escaped_title.replace(' ', '-').replace('---', '-').replace('.','').replace(':','')
    return '/post/' + str(post_id) + '/' + link_title + '.html'
  