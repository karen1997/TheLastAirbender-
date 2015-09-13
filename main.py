#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import logging
import os
from google.appengine.api import users
from google.appengine.ext import ndb
import json

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#stores data for the Doctors
class DoctorUser(ndb.Model):
    doctorName = ndb.StringProperty()
    doctorLanguage = ndb.StringProperty(repeated=True)
    doctorLocation = ndb.StringProperty()

#stores data for the Patients
class PatientUser(ndb.Model):
    patientName = ndb.StringProperty()
    patientLanguage = ndb.StringProperty(repeated=True)
    patientLocation = ndb.StringProperty()


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/homepage.html')
        self.response.write(template.render())

class DoctorHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/doctoraccount.html')
        self.response.write(template.render())

    #retrieves User information from email login and stores users input
    def post(self):
        currUser = users.get_current_user()
        currEmail = currUser.email()
        name = self.request.get('name')
        languageList = []
        language = self.request.get('language')
        languageList = language.split()
        logging.info(languageList)
        location = self.request.get('location')
        user = DoctorUser (id = currEmail,
                           doctorName = name,
                           doctorLanguage = languageList,
                           doctorLocation = location)
        user.put()


class PatientHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/patientaccount.html')
        self.response.write(template.render())

    def post(self):
        currUser = users.get_current_user()
        currEmail = currUser.email()
        name = self.request.get('name1')
        languageList = []
        language = self.request.get('language1')
        languageList = language.split()
        location = self.request.get('location1')
        user = PatientUser (id = currEmail,
                            patientName = name,
                            patientLanguage = languageList,
                            patientLocation = location)
        user.put()

class ResultsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/results.html')
        self.response.write(template.render())

    def post(self):
        template = jinja_environment.get_template('templates/results.html')
        self.response.write(template.render())

class DocloginHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/doctorlogin.html')
        self.response.write(template.render())

class PatloginHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/patientlogin.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/doctoraccount', DoctorHandler),
    ('/patientaccount', PatientHandler),
    ('/results', ResultsHandler),
    ('/doctorlogin', DocloginHandler),
    ('/patientlogin', PatloginHandler),
], debug=True)
