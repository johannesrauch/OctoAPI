#!/usr/bin/env python

# ------------------------------------------------------------------------------------------------
# Autor: Johannes Rauch
# Datum: 08.05.17
#
# This is a library that allows you to use the octoprint api simply through functions.
# You are able to get printer, job or file informations or issue several commands to it. 
#
# to do:
# upload a file or create folder
# ------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------------------------

import json
import requests
import os
import logging

# ------------------------------------------------------------------------------------------------
# global variables
# ------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------
# classes
# ------------------------------------------------------------------------------------------------
		
class OctoPrint_API(object):
	def __init__(self):
		self._config = self._load_config()
		self._session = None
		
	@property
	def config(self):
		return self._config
		
	@property
	def key(self):
		return self._config["OctoAPI_KEY"]
		
	@property
	def session(self):
		if not self._session:
			self._session = requests.Session()
			self._session.headers["X-Api-Key"] = self.key
			self._session.headers["Content-Type"] = "application/json"
			self._session.keep_alive = False
		return self._session

	@property
	def url(self):
		return (self.config["OctoPrint_URL"] + "/api/")
		
	def _load_config(self):
		home_dir = os.path.expanduser("~")
		config_path = os.path.join(home_dir, ".octoapi.conf")
		try:
			config_file = open(config_path)
			config = json.loads(config_file.read())
			config_file.close()
			return config
		except FileNotFoundError:
			logging.warning("Found no config!")
		return {}
			
	def check_response(self, res, code, transform = False):
		# check code
		if code != res.status_code:
			logging.warning("status_code:\t{}".format(res.status_code))
			logging.warning("text:\t\t{}".format(res.text))
			return None
		# transform response to dict
		if transform:
			try:
				res = res.json()
			except ValueError:
				logging.warning("Failed .json convertion!")
				res = None
		return res
			
	def get(self, **kwargs):
		res = self.session.get(self.url + kwargs["url"], params = kwargs)
		return self.check_response(res, 200, True)
		
	def post(self, **kwargs):
		payload = json.dumps(kwargs)
		res = self.session.post(self.url + kwargs["url"], data = payload)
		return self.check_response(res, 204)
		
# ------------------------------------------------------------------------------------------------
# functions
# ------------------------------------------------------------------------------------------------
	
def get_bed_dict():
	kwargs = {"url": "printer/bed"}
	return retrieve(**kwargs)
	
def get_completion():
	return get_job_dict()["progress"]["completion"]
	
def get_connection_dict():
	kwargs = {"url": "connection"}
	return retrieve(**kwargs)
	
def get_files_dict(recursive = False, path = ""):
	kwargs = {"recursive": recursive, "url": "files" + path}
	return retrieve(**kwargs)
	
def get_job_dict():
	kwargs = {"url": "job"}
	return retrieve(**kwargs)
	
def get_logs_dict():
	kwargs = {"url": "logs"}
	return retrieve(**kwargs)
	
def get_printer_dict():
	kwargs = {"url": "printer"}
	return retrieve(**kwargs)
	
def get_printerprofiles_dict():
	kwargs = {"url": "printerprofiles"}
	return retrieve(**kwargs)
	
def get_printTime():
	return get_job_dict()["progress"]["printTime"]
	
def get_printTimeLeft():
	return get_job_dict()["progress"]["printTimeLeft"]
	
def get_sd_dict():
	kwargs = {"url": "printer/sd"}
	return retrieve(**kwargs)
	
def get_setting_dict():
	kwargs = {"url": "settings"}
	return retrieve(**kwargs)
	
def get_systemCommands_dict(source = ""):
	kwargs = {"url": "system/commands" + source}
	return retrieve(**kwargs)
	
def get_tool_dict():
	kwargs = {"url": "printer/tool"}
	return retrieve(**kwargs)
	
def get_users_dict(user = ""):
	kwargs = {"url": "users" + user}
	return retrieve(**kwargs)
	
def get_version_dict():
	kwargs = {"url": "version"}
	return retrieve(**kwargs)
	
def issue(**kwargs):
	op = OctoPrint_API()
	return op.post(**kwargs)
	
def post_cancel():
	kwargs = {"command": "cancel", "url": "job"}
	return issue(**kwargs)
	
def post_connect(port = None, baudrate = None, printerProfile = None, save = False, autoconnect = True):
	kwargs = {"command": "connect", "save": save, "autoconnect": autoconnect, "url": "connection"}
	if port:
		kwargs["port"] = port
	if baudrate:
		kwargs["baudrate"] = baudrate
	if printerProfile:
		kwargs["printerProfile"] = printerProfile
	return issue(**kwargs)
	
def post_copy(file, destination):
	kwargs = {"command": "copy", "destination": destination, "url": "files/local" + file}
	return issue(**kwargs)
	
def post_disconnect():
	kwargs = {"command": "disconnect", "url": "connection"}
	return issue(**kwargs)
	
def post_fake_ack():
	kwargs = {"command": "fake_ack", "url": "connection"}
	
def post_home(*args):
	kwargs = {"axes": args, "command": "home", "url": "printer/printhead"}
	return issue(**kwargs)

def post_print(file):
	kwargs = {"command": "select", "print": True, "url": "files/local" + file}
	return issue(**kwargs)
	
def post_select(file):
	kwargsargs = {"command": "select", "url": "files/local" + file}
	return issue(**kwargs)
	
def retrieve(**kwargs):
	op = OctoPrint_API()
	return op.get(**kwargs)

# ------------------------------------------------------------------------------------------------
# main - for debugging purposes
# ------------------------------------------------------------------------------------------------

def _main():
	#print(get_completion())
	#print(get_connection_dict())
	#print(get_files_dict())
	#print(get_job_dict())
	#print(get_printer_dict())
	#print(get_printTime())
	#print(get_printTimeLeft())
	print(get_users_dict())
	#print(get_version_dict())
	#print(post_cancel())
	#print(post_home("x", "y"))
	#print(post_print("LCD_case.gcode"))
	pass

if __name__ == "__main__":
	_main()
