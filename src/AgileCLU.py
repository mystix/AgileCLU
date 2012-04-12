#!/usr/bin/python
# Filename: AgileCLU.py
# coding: utf-8
#
# Copyright (C) 2010-2011, Wylie Swanson
#
# This Program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License V3, as published by
# the Free Software Foundation.
#
# This Program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

from jsonrpc import ServiceProxy
import ConfigParser, sys, os.path, logging
import poster 
from urllib2 import Request, urlopen, URLError, HTTPError

logger = logging.getLogger('AgileCLU')
hdlr = logging.FileHandler( '/var/log/agileclu.log' )
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


cfg = ConfigParser.ConfigParser() 
version = '0.2'

class	AgileCLU:

        def     __init__(self, username='agile'):

		# Load configuration variables

		if os.path.exists('/etc/agile/'+username+'.conf'): cfg.read('/etc/agile/'+username+'.conf')
		else:
			print "Alternate login identity (%s) configuration does not exist.  Exiting." % username
			logger.critical( "configuration /etc/agile/"+username+".conf does not exist" )
			sys.exit(1)

		self.uid = cfg.get("Identity", "username")
		upw = cfg.get("Identity", "password")
		self.apiurl = cfg.get("Ingest", "apiurl")
		self.posturl = cfg.get("Ingest", "posturl")
		self.mapperurl = cfg.get("Egress", "mapperurl")
		self.cacheurl = cfg.get("Egress", "mapperurl")

		# connect to API, authenticate, and get a token

		self.api = ServiceProxy( self.apiurl )
		self.token, self.user = self.api.login( self.uid, upw )
		if self.token is None:
			print "Autentication for '"+str(self.uid)+"' failed. Please check credentials.  Exiting."
			logger.critical( self.uid+" login failed - check account credentials" )
			sys.exit(1)

		logger.info( self.uid+" "+self.token+", login "+str(self.user)+" tokenized" )
	
	def	apiurlstr(self):
		logger.info( self.uid+" "+self.token+", apiurl="+self.apiurl )
		return self.apiurl

	def	posturlstr(self):
		logger.info( self.uid+" "+self.token+", posturl="+self.posturl )
		return self.posturl

	def	mapperurlstr(self):
		logger.info( self.uid+" "+self.token+", mapperurl="+self.mapperurl )
		return self.mapperurl

	def	cacheurlstr(self):
		logger.info( self.uid+" "+self.token+", cacheurl="+self.cacheurl )
		return self.cacheurl

	def	tokenstr(self):
		logger.info( self.uid+" "+self.token+", self.token" )
		return self.token

	def	stat(self, path):
		r = self.api.stat( self.token, path )
		logger.info( self.uid+" "+self.token+", stat "+path+" = "+str(r) )
		return r

	def	logout(self):
		r = self.api.logout( self.token )
		logger.info( self.uid+" "+self.token+", logout = "+str(r)+", detokenized" )
		return r

	def	noop(self):
		r = self.api.noop( self.token )
		logger.info( self.uid+" "+self.token+", noop = "+str(r) )
		return r

	def	listDir(self, path, pageSize=10000, cookie=0, stat=True ):
		r = self.api.listDir( self.token, path, pageSize, cookie, stat )
		logger.info( self.uid+" "+self.token+", listDir "+path+" pageSize "+str(pageSize)+" cookie "+str(cookie)+" stat "+str(stat) )
		# +" = "+str(r) )
		return r

	def	listFile(self, path, pageSize=10000, cookie=0, stat=True ):
		r = self.api.listFile( self.token, path, pageSize, cookie, stat )
		logger.info( self.uid+" "+self.token+", listFile "+path+" pageSize "+str(pageSize)+" cookie "+str(cookie)+" stat "+str(stat) )
		# +" = "+str(r) )
		return r

	def	makeDir(self, path):
		r = self.api.makeDir( self.token, path)
		logger.info( self.uid+" "+self.token+", makeDir "+path+" = "+str(r) )
		return r

	def	makeDir2(self, path):
		r = self.api.makeDir2( self.token, path)
		logger.info( self.uid+" "+self.token+", makeDir2 "+path+" = "+str(r) )
		return r

	def	deleteFile(self, path):
		r = self.api.deleteFile( self.token, path)
		logger.info( self.uid+" "+self.token+", deleteFile "+path+" = "+str(r) )
		return r

	def	rm(self, path):
		if (self.fexists(path)):
			r = self.deleteFile(path)
			if (r == 0): 
				logger.info( self.uid+" "+self.token+", rm "+path+" succeeded" )
				return True
			else: 
				logger.warning( self.uid+" "+self.token+", rm "+path+" failed" )
				return False
		else:
			logger.warning( self.uid+" "+self.token+", rm "+path+" skipped nonexistent file" )

	def	deleteDir(self, path):
		r = self.api.deleteDir( self.token, path)
		logger.info( self.uid+" "+self.token+", deleteDir "+path+" = " + str(r) )
		return r

	def	deleteObject(self, path):
		r = self.api.deleteObject( self.token, path)
		logger.info( self.uid+" "+self.token+", deleteObject "+path+" = " + str(r) )
		return r

	def	rename(self, path, newpath):
		r = self.api.rename( self.token, path, newpath)
		logger.info( self.uid+" "+self.token+", rename "+path+" to "+newpath+" = " + str(r) )
		return r
	
	def	copyFile(self, path, newpath):
		r = self.api.copyFile( self.token, path, newpath)
		logger.info( self.uid+" "+self.token+", copyFile "+path+" to "+newpath+" = " + str(r) )
		return r

	def	registerCallback( self, uri, flags=0, threshold=0 ):
		r = self.api.registerCallback( self.token, uri, flags, threshold )
		logger.info( self.uid+" "+self.token+", registerCallback "+uri+" flags "+str(flags)+" threshold "+str(threshold)+" = " + str(r) )
		return r

	def	listCallback( self ):
		r = self.api.listCallback( self.token )
		logger.info( self.uid+" "+self.token+", listCallback" )
		return r

	def	fetchFileHTTP( self, path, uri, username=None, password=None, auth=None, callbackid=0, priority=0, flags=0, expose_egress='COMPLETE'):
		r = self.api.fetchFileHTTP( self.token, path, uri, username, password, auth, callbackid, priority, flags, expose_egress)
		logger.info( self.uid+" "+self.token+", fetchFileHTTP path "+path+" uri "+uri+" username "+str(username)+" auth "+str(auth)+" callbackid "+str(callbackid)+" priority "+str(priority)+" flags "+str(flags)+" expose_egress "+expose_egress+" = " + str(r) )
		return r

	def	fetchFileFTP(self, path, hostname, filename, username=None, password=None, port=21, passive=True, callbackid=0, priority=0, flags=0, expose_egress='COMPLETE'):
		r = self.api.fetchFileFTP( self.token, path, hostname, filename, username, password, port, passive, callbackid, priority, flags, expose_egress)
		logger.info( self.uid+" "+self.token+", fetchFileFTP path "+path+" hostname "+hostname+" filename "+filename+" username "+str(username)+" port "+str(port)+" passive "+str(passive)+" callbackid "+str(callbackid)+" priority "+str(priority)+" flags "+str(flags)+" expose_egress "+expose_egress+" = " + str(r) )
		return r

	def	fexists( self, path ):
		r = self.stat( path )
		logger.info( self.uid+" "+self.token+", fexists "+path+" = "+str(r) )
		if ((r['code'] == 0) and (r['type'] == 2)): return True
		else: return False

	def	dexists( self, path ):
		r = self.stat( path )
		logger.info( self.uid+" "+self.token+", dexists "+path+" = "+str(r) )
		if ((r['code'] == 0) and (r['type'] == 1)): return True
		else: return False

	def	exists(self, path):
		logger.info( self.uid+" "+self.token+", exists "+path )
		# +" = "+str(r) )
		if (self.fexists(path) or self.dexists(path)): return True
		else: return False

	def	mkdir(self, path, recursive = False):
		logger.info( self.uid+" "+self.token+", mkdir "+path )
		# +" = "+str(r) )
		if (not self.dexists(path)):
			if (recursive):
				r = self.makeDir2( path )
			else:
				r = self.makeDir( path )
			if (r == 0): 
				return True
			else: 
				return False
		else:	
			return False

	def	read(self, path):
		logger.info( self.uid+" "+self.token+", read "+self.mapper.url+urllib2.quote(path) )
		if (self.fexists(path)):
			response = urllib2.urlopen( self.mapperurl+urllib2.quote(path) )
			return response.read()
		else:
			return False

	def	post(self, source, destination, rename=None, mimetype='auto', mtime=None, egress_policy='COMPLETE', mkdir=False, callback=None):
		logger.info( self.uid+" "+self.token+", post "+source+" "+destination+", rename="+str(rename)+", mimetype="+str(mimetype)+", mtime="+str(mtime)+", egress="+str(egress_policy)+", mkdir="+str(mkdir))
		if (not os.path.isfile(source)): logger.info( "local("+source+") does not exist") ; return False 
		if (not self.dexists(destination)): logger.info( "remote("+destination+") does not exist") ; return False

		source_path = os.path.dirname(source) ; source_name = os.path.basename(source)
	
		poster.streaminghttp.register_openers()
	
		if callback<>None:
			datagen, headers = poster.encode.multipart_encode( {
				"uploadFile": open(source, "rb"),
				"directory": destination,
				"basename": source_name,
				"expose_egress": egress_policy
				}, cb=callback)
		else:
			datagen, headers = poster.encode.multipart_encode( {
				"uploadFile": open(source, "rb"),
				"directory": destination,
				"basename": source_name,
				"expose_egress": egress_policy
				} )

		request = Request(self.posturl, datagen, headers)
		request.add_header("X-LLNW-Authorization", self.token)
		request.add_header("X-Content-Type", mimetype )

		try: result = urlopen(request).read()
		except HTTPError, e: logger.info( 'HTTP Error: '+str(e.code) ) ; return False
		except URLError, e: logger.info( 'URL Error: '+str(e.reason) ) ; return False

		return True

# End of agile.py
