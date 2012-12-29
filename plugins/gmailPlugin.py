import logging
import sys
import plugin_def
import action_def
import imaplib
import random
import copy
import time
import email
import nltk

import xoauth
#TODO: find a way to handle per-user prefs

PLUGIN_NAME = 'gmail'
PLUGIN_PREFS = ['interval', 'mark_as_read', 'email', 'token', 'secret']

MY_EMAIL = ''
MY_TOKEN = ''  # your token
MY_SECRET = ''                      # your secret

class newMailEvent(action_def.Event):
   def __init__(self):
      super(newMailEvent,self).__init__("gmailEventType", "newMailEvent")
      self.addParameter("from")
      self.addParameter("subject")
      self.addParameter("body")

#TO become sendMailAction
class gmailAction(action_def.Action):
   def __init__(self, gmailPlugin):
      super(gmailAction,self).__init__("gmailAction", "gmailAction1", gmailPlugin)
   def __call__(self, args={}):
      logging.warning("gmail from gmailAction! %s", args);

class gmailPlugin(plugin_def.Plugin):
   
   def __init__(self):
      super(gmailPlugin,self).__init__(PLUGIN_NAME);
      self.addAction(gmailAction(self))
      self.addEvent(newMailEvent())
      #self.conn = self.connect() #TOFIX with user preferences
      self.finished = 1 #TOFIX along the rest (reput to 0)
      ####
      # PLUGIN PREFERENCES
      ####
      self.interval = 90 #time interval between 2 mail checks #REALISTIC
      self.interval = 2  #time interval between 2 mail checks #FOR DEBUG
      self.mark_as_read = 0 #mark emails seen as read

   def connect(self):
      nonce = str(random.randrange(2**64 - 1))
      timestamp = str(int(time.time()))

      consumer = xoauth.OAuthEntity('anonymous', 'anonymous')
      access = xoauth.OAuthEntity(MY_TOKEN, MY_SECRET)
      token = xoauth.GenerateXOauthString(
            consumer, access, MY_EMAIL, 'imap', MY_EMAIL, nonce, timestamp)

      imap_conn = imaplib.IMAP4_SSL('imap.googlemail.com')
      imap_conn.debug = 4
      imap_conn.authenticate('XOAUTH', lambda x: token)
      imap_conn.select('INBOX')

      return imap_conn

   def run(self):
      while (not self.finished):
         (retcode, messages) = self.conn.search(None, '(UNSEEN)')
         if retcode == 'OK':
            for message in messages[0].split(' '):
               if (message != ''):
                  logging.info('Processing : %s', message)
                  #fetch only the subject, not marking the mail as read
                  (ret, mesginfo) = self.conn.fetch(message, '(RFC822.SIZE BODY.PEEK[HEADER.FIELDS (SUBJECT)])')
                  if ret == 'OK':
                     subject = mesginfo[0][1] #contains "Subject: "+actual subject
                     logging.info(mesginfo)
                  (ret, mesginfo) = self.conn.fetch(message, '(RFC822.SIZE BODY.PEEK[HEADER.FIELDS (FROM)])')
                  if ret == 'OK':
                     fromstr = mesginfo[0][1] #contains "Subject: "+actual subject
                     logging.info(mesginfo)

                  #now fetch the whole thing
                  msg_str = ""
                  if (self.mark_as_read):
                     (ret, mesginfo_body) = self.conn.fetch(message, '(RFC822)')
                     msg_str = mesginfo_body[0][1]
                  else :
                     # PEEK doesn't mark as read
                     (ret, mesginfo_body1) = self.conn.fetch(message, '(BODY.PEEK[HEADER])')
                     (ret, mesginfo_body ) = self.conn.fetch(message, '(BODY.PEEK[TEXT])')
                     msg_str = mesginfo_body1[0][1]+mesginfo_body[0][1]
                  if ret == 'OK':
                     mail = email.message_from_string(msg_str)
                     bodytext = ""
                     for part in mail.walk():
                        if (part.get_content_type() == 'text/plain'):
                           bodytext = part.get_payload(decode = True)
                        elif (part.get_content_type() == 'text/html'):
                           bodystring = nltk.clean_html(part.get_payload(decode=True)) #strip html
                     if (bodytext == ""):
                        bodytext = bodystring #if there's no text, then get the stripped html version 

                     evt = newMailEvent()
                     evt.eventArgs = {'mail':copy.copy(fromstr)+copy.copy(subject)+copy.copy(bodytext)}
                     evt.eventArgs = {'from':copy.copy(fromstr)}
                     evt.eventArgs = {'subject':copy.copy(subject)}
                     evt.eventArgs = {'body':copy.copy(bodytext)}
                     self.post(evt)
                     logging.info("newMail:"+bodytext)
                     logging.debug(msg_str)
         time.sleep(self.interval)

   def stop(self):
      self.finished = 1
      self.conn.close()


