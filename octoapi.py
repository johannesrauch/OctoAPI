#!/usr/bin/env python

# ------------------------------------------------------------------------------------------------
# Autor: Johannes Rauch
# Datum: 08.05.17
#
# This is a library that allows you to use the octoprint api simply through functions.
# You are able to get printer, job or file informations or issue several commands to it. 
#
# to do:
# - upload a file or create folder
# - execute a registered system command; response code = 204
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
	def session(self, content_type = "application/json"):
		if not self._session:
			self._session = requests.Session()
			self._session.headers["X-Api-Key"] = self.key
			self._session.headers["Content-Type"] = content_type
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
		except IOError:
			logging.warning("Found no config!")
		return {}
			
	def check_response(self, res, code, transform = False):
		# check code
		if code != res.status_code:
			logging.warning("status_code:\t{}".format(res.status_code))
			logging.warning("text:\t\t{}".format(res.text))
			return res
		# transform response to dict
		if transform:
			try:
				res = res.json()
			except ValueError:
				logging.warning("Failed .json convertion!")
				res = None
		return res
			
	def get(self, **kwargs):
		code = kwargs["code"] if "code" in kwargs else 200
		res = self.session.get(self.url + kwargs["url"], params = kwargs)
		return self.check_response(res, code, True)
		
	def post(self, **kwargs):
		code = kwargs["code"] if "code" in kwargs else 200
		payload = json.dumps(kwargs)
		res = self.session.post(self.url + kwargs["url"], data = payload)
		return self.check_response(res, code)
		
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
	
def is_printing():
	return get_printer_dict()["state"]["flags"]["printing"]
	
def issue(**kwargs):
	op = OctoPrint_API()
	return op.post(**kwargs)
	
def post_bed(**kwargs):
	kwargs.update({"url": "printer/bed", "code": 204})
	return issue(**kwargs)
	
def post_cancel():
	kwargs = {"command": "cancel"}
	return post_job(**kwargs)
	
def post_command(*args):
	kwargs = {"commands": args, "url": "printer/command", "code": 204}
	return issue(**kwargs)
	
def post_connect(**kwargs):
	kwargs.update({"command": "connect"})
	return post_connection(**kwargs)
	
def post_connection(**kwargs):
	kwargs.update({"url": "connection", "code": 204})
	return issue(**kwargs)
	
def post_copy(file, destination):
	kwargs = {"command": "copy", "destination": destination, "url": "files/local/" + file, "code": 201}
	return issue(**kwargs)
	
def post_disconnect():
	kwargs = {"command": "disconnect"}
	return post_connection(**kwargs)
	
def post_extrude(amount):
	kwargs = {"command": "extrude", "amount": amount}
	return post_tool(**kwargs)
	
def post_fake_ack():
	kwargs = {"command": "fake_ack"}
	return post_connection(**kwargs)
	
def post_feedrate(factor):
	factor = 50 if factor < 50 else factor
	factor = 200 if factor > 200 else factor
	kwargs = {"command": "feedrate", "factor": factor}
	return post_printhead(**kwargs)
	
def post_flowrate(factor):
	factor = 75 if factor < 75 else factor
	factor = 125 if factor > 125 else factor
	kwargs = {"command": "flowrate", "factor": factor}
	return post_tool(**kwargs)
	
def post_home(*args):
	kwargs = {"command": "home", "axes": args}
	return post_printhead(**kwargs)
	
def post_init_sd():
	kwargs = {"command": "init"}
	return post_sd(**kwargs)
	
def post_job(**kwargs):
	kwargs.update({"url": "job", "code": 204})
	return issue(**kwargs)
	
def post_jog(x = 0, y = 0, z = 0, absolute = False, speed = False):
	kwargs = {"command": "jog", "x": x, "y": y, "z": z, "absolute": absolute, "speed": speed}
	return post_printhead(**kwargs)
	
def post_move(file, destination):
	kwargs = {"command": "move", "destination": destination, "url": "files/local/" + file, "code": 201}
	return issue(**kwargs)
	
def post_offset_bed(offset):
	kwargs = {"command": "offset", "offset": offset}
	return post_bed(**kwargs)
	
def post_offset_tools(**kwargs):
	kwargs.update({"command": "offset"})
	return post_tool(**kwargs)
	
def post_offset_tool0(offset):
	return post_offset_tools(offsets = {"tool0": offset})

def post_pause(action = "pause"):
	kwargs = {"command": "pause", "action": action}
	return post_job(**kwargs)

def post_print(file):
	kwargs = {"command": "select", "print": True, "url": "files/local/" + file, "code": 204}
	return issue(**kwargs)
		
def post_printerprofile(**kwargs):
	kwargs.update({"url": "printerprofiles"})
	return issue(**kwargs)
	
def post_printhead(**kwargs):
	kwargs.update({"url": "printer/printhead", "code": 204})
	return issue(**kwargs)
	
def post_refresh_sd():
	kwargs = {"command": "refresh"}
	return post_sd(**kwargs)
	
def post_release_sd():
	kwargs = {"command": "release"}
	return post_sd(**kwargs)
	
def post_restart():
	kwargs = {"command": "restart"}
	return post_job(**kwargs)
	
def post_sd(**kwargs):
	kwargs.update({"url": "printer/sd", "code": 204})
	return issue(**kwargs)
	
def post_select_file(file, start_print = False):
	kwargs = {"command": "select", "print": start_print, "url": "files/local/" + file, "code": 204}
	return issue(**kwargs)
	
def post_select_tool(tool):
	kwargs = {"command": "select", "tool": tool}
	return post_tool(**kwargs)
	
def post_settings(**kwargs):
	kwargs.update({"url": "settings"})
	return issue(**kwargs)
	
def post_start():
	kwargs = {"command": "start"}
	return post_job(**kwargs)
	
def post_system():
	pass
	
def post_target_bed(target):
	kwargs = {"command": "target", "target": target}
	return post_bed(**kwargs)
	
def post_target_tools(**kwargs):
	kwargs.update({"command": "target"})
	return post_tool(**kwargs)
	
def post_target_tool0(target):
	target = 0 if target < 0 else target
	target = 220 if target > 220 else target
	return post_target_tools(targets = {"tool0": target})
	
def post_tool(**kwargs):
	kwargs.update({"url": "printer/tool", "code": 204})
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
	#print(get_users_dict())
	#print(get_version_dict())
	#print(post_cancel())
	#print(post_home("x", "y"))
	#print(post_print("LCD_case.gcode"))
	pass

if __name__ == "__main__":
	_main()