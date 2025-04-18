#!/usr/bin/python
import os
import datetime
import logging
import math
import sys
import plistlib
import string
import struct
import xml.parsers.expat
import subprocess
import json
import socket
import Foundation
import Quartz
import argparse
import ctypes
import ctypes.util
import objc
import platform
import time
import hashlib
import sqlite3
import tempfile
import shutil
import binascii
import urllib2
import urllib
import base64
import hmac
import httplib
import urllib
import time
import random
import threading


# send the hash to VirusTotal for checking
vtResultRequested = False
attempts = 0
maxAttempts = 5759

#get the hostname of the system the script is running on
hostname = socket.gethostname()

#get UUID - https://apple.stackexchange.com/questions/72355/how-to-get-uuid-with-python/72360#72360
def getUUID():
  from Foundation import NSBundle
  IOKit_bundle = NSBundle.bundleWithIdentifier_('com.apple.framework.IOKit')
  functions = [("IOServiceGetMatchingService", b"II@"),
             ("IOServiceMatching", b"@*"),
             ("IORegistryEntryCreateCFProperty", b"@I@@I"),
            ]
  objc.loadBundleFunctions(IOKit_bundle, globals(), functions)
  def io_key(keyname):
    return IORegistryEntryCreateCFProperty(IOServiceGetMatchingService(0, IOServiceMatching("IOPlatformExpertDevice".encode("utf-8"))), keyname, None, 0)

  #return the system's unique identifier
  return str(io_key("IOPlatformUUID".encode("utf-8")))

#uuid saved to variable
UUID = getUUID()

#get system information from the os
def getSystemInfo(output_file):
  print("%s" % "[+] Getting system information.")
  system_data = {}
  uname = os.uname()
  macos_version = platform.mac_ver()[0]
  macos_arch = platform.mac_ver()[2]
  system_data.update({'hostname':uname[1]})
  system_data.update({'UUID':UUID})
  system_data.update({'kernel':uname[2]})
  system_data.update({'kernel_release':uname[3].split(';')[1].split(':')[1]})
  system_data.update({'macOS_version':macos_version})
  system_data.update({'macOS_arch':macos_arch})
  system_data.update({"module":"system_info"})
  json.dump(system_data,output_file)
  outfile.write("\n")

def getVTResult(fileHash):
  global attempts
  global maxAttempts

  if attempts % 4 == 0:
    time.sleep(60)

  if vtResultRequested:
    while attempts < maxAttempts:
      req = "/vtapi/v2/file/report?apikey={}&resource={}".format(vtAPIKey, fileHash)
      con = httplib.HTTPSConnection("www.virustotal.com")
      con.request("GET", req)
      r = con.getresponse()
      if r.status != 429:
        if r.status == 200:
          respBody = json.loads(r.read())
          attempts = attempts + 1
          if respBody['response_code'] == 0:
            return "This file has no VirusTotal entry."
          else:
            if respBody['positives'] != 0:
              return "POSITIVE VT SCAN - see " + respBody['permalink']
            else:
              return "This file is OK."

    return "shouldnt get here"


# get the sha256 hash of any file
def getHash(file, ignoreVFlag):
    hasher = hashlib.sha256()
    if os.path.exists(file) and os.path.isfile(file):
        with open(file, 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
            fileHash = hasher.hexdigest()
    else:
        fileHash = "File is a directory or doesn't exist"

    # send hash to Virustotal if requested. Doing it here will help with the 4 queries/minute rate limit
    if ignoreVFlag == True:
      vt_res = "Ignored"
    else:
      vt_res = getVTResult(fileHash)

    return(fileHash, vt_res)

#Code used from https://github.com/synack/knockknock/blob/master/knockknock.py - Patrick Wardle! - to get the signing information for a given executable
def checkSignature(file, bundle=None):
  SECURITY_FRAMEWORK = '/System/Library/Frameworks/Security.framework/Versions/Current/Security'
  kSecCSDefaultFlags = 0x0
  kSecCSDoNotValidateResources = 0x4
  kSecCSCheckAllArchitectures = 0x1
  kSecCSCheckNestedCode = 0x8
  kSecCSStrictValidate = 0x16
  kSecCSStrictValidate_kSecCSCheckAllArchitectures = 0x17
  kSecCSStrictValidate_kSecCSCheckAllArchitectures_kSecCSCheckNestedCode = 0x1f
  errSecSuccess = 0x0
  SecCSSignatureOK = errSecSuccess
  errSecCSUnsigned = -67062
  kPOSIXErrorEACCES = 100013
  kSecCSSigningInformation = 0x2
  kSecCodeInfoCertificates = 'certificates'

	#return dictionary
  signingInfo = {}
  sigCheckFlags = kSecCSStrictValidate_kSecCSCheckAllArchitectures_kSecCSCheckNestedCode
  securityFramework = ctypes.cdll.LoadLibrary(SECURITY_FRAMEWORK)
  objcRuntime = ctypes.cdll.LoadLibrary(ctypes.util.find_library('objc'))
  objcRuntime.objc_getClass.restype = ctypes.c_void_p
  objcRuntime.sel_registerName.restype = ctypes.c_void_p
  status = not errSecSuccess
  signedStatus = None
  isApple = False
  authorities = []

  file = Foundation.NSString.stringWithString_(file)
  file = file.stringByAddingPercentEscapesUsingEncoding_(Foundation.NSUTF8StringEncoding).encode('utf-8')
  path = Foundation.NSURL.URLWithString_(Foundation.NSString.stringWithUTF8String_(file))
  staticCode = ctypes.c_void_p(0)
  result = securityFramework.SecStaticCodeCreateWithPath(ctypes.c_void_p(objc.pyobjc_id(path)), kSecCSDefaultFlags, ctypes.byref(staticCode))
  signedStatus = securityFramework.SecStaticCodeCheckValidityWithErrors(staticCode, sigCheckFlags,None, None)
  if errSecSuccess == signedStatus:
    requirementReference = "anchor apple"
    NSString = objcRuntime.objc_getClass('NSString')
    objcRuntime.objc_msgSend.restype = ctypes.c_void_p
    objcRuntime.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
    requirementsString = objcRuntime.objc_msgSend(NSString, objcRuntime.sel_registerName('stringWithUTF8String:'), requirementReference)
    requirement = ctypes.c_void_p(0)
    if errSecSuccess == securityFramework.SecRequirementCreateWithString(ctypes.c_void_p(requirementsString), kSecCSDefaultFlags, ctypes.byref(requirement)):
        if errSecSuccess == securityFramework.SecStaticCodeCheckValidity(staticCode, sigCheckFlags, requirement):
            isApple = True

    information = ctypes.c_void_p(0)
    result = securityFramework.SecCodeCopySigningInformation(staticCode, kSecCSSigningInformation,ctypes.byref(information))
    objcRuntime.objc_msgSend.restype = ctypes.c_void_p
    objcRuntime.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
    key = objcRuntime.objc_msgSend(NSString, objcRuntime.sel_registerName('stringWithUTF8String:'), kSecCodeInfoCertificates)
    objcRuntime.objc_msgSend.restype = ctypes.c_void_p
    objcRuntime.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
    certChain = objcRuntime.objc_msgSend(information, objcRuntime.sel_registerName('objectForKey:'), key)
    objcRuntime.objc_msgSend.restype = ctypes.c_uint
    objcRuntime.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    count = objcRuntime.objc_msgSend(certChain, objcRuntime.sel_registerName('count'))
    certName = ctypes.c_char_p(0)
    for index in range(count):
        objcRuntime.objc_msgSend.restype = ctypes.c_void_p
        objcRuntime.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint]
        cert = objcRuntime.objc_msgSend(certChain, objcRuntime.sel_registerName('objectAtIndex:'), index)
        result = securityFramework.SecCertificateCopyCommonName(ctypes.c_void_p(cert), ctypes.byref(certName))
        if errSecSuccess != result:
            continue
        objcRuntime.objc_msgSend.restype = ctypes.c_char_p
        objcRuntime.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        authorities.append(objcRuntime.objc_msgSend(certName, objcRuntime.sel_registerName('UTF8String')))

  status = errSecSuccess
  if signedStatus == 0:
    signingInfo['status'] = "signed"
  else:
    signingInfo['status'] = "unsigned"
  signingInfo['apple_binary'] = isApple
  signingInfo['Authority'] = authorities
  return (signingInfo)

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()

def parseAgentsDaemons(item,path):
  parsedPlist = {}
  plist_file = path+"/"+item
  try:
    plist_type = subprocess.Popen(["file", plist_file], stdout=subprocess.PIPE).communicate()
  except:
    parsedPlist.update({"Plist_file_error":"File does not exist or can not be accessed."})
    return parsedPlist
  #get the plist type
  plist_type = plist_type[0].split(":")[1].strip("\n").strip(" ")
  #if else the file is a binary plist, then we have to use external library to parse
  try:
    if plist_type == 'Apple binary property list':
        plist = Foundation.NSDictionary.dictionaryWithContentsOfFile_(plist_file)
    #elif plist_type == 'XML 1.0 document text, ASCII text':
      #plist = plistlib.readPlist(plist_file)
    elif plist_type == 'exported SGML document text, ASCII text':
      plist_text = subprocess.Popen(["cat", plist_file], stdout=subprocess.PIPE).communicate()
      #plist_text = plist_text[0].split("\n")
      if plist_text[0].split("\n")[0].startswith("<?xml"):
        plist = plistlib.readPlistFromString(plist_text)
      else:
        xml_start = plist_text[0].find('<?xml')
        plist_string = plist_text[0][xml_start:]
        plist = plistlib.readPlistFromString(plist_string)
    else:
      plist = plistlib.readPlist(plist_file)
  except:
      parsedPlist.update({'plist_format_error': ("Error parsing %s with hash %s" % (plist_file,getHash(plist_file)))})
      return parsedPlist

  progExecutableHash = ""
  progExecutable = ""
  progVTResult = ""
  try:
    if plist.get("ProgramArguments"):
      progExecutable = plist.get("ProgramArguments")[0]
      if os.path.exists(progExecutable):
        try:
          progExecutableHash, progVTResult = getHash(progExecutable)
        except:
          progExecutableHash = "Error hashing "+progExecutable
          progVTResult = "No VT result"
    elif plist.get("Program"):
      progExecutable = plist.get("Program")
      progExecutableHash, progVTResult = getHash(progExecutable)
      if progExecutable.startswith('REPLACE_HOME'):
        findHomeStart = plist_file.find("/Library")
        progExecutable = progExecutable.replace('REPLACE_HOME',plist_file[:findHomeStart])
        progExecutableHash, progVTResult = getHash(progExecutable)
  except:
    progExecutable = "Error parsing or no associated executable"
    progExecutableHash = "No executable to parse"
    progVTResult = "No VT result"

  if plist:
    if plist.get("RunAtLoad"):
      parsedPlist.update({'runAtLoad': str(plist.get("RunAtLoad"))})

    parsedPlist.update({'label': str(plist.get("Label"))})
    parsedPlist.update({'program': str(plist.get("Program"))})
    parsedPlist.update({'program_arguments': (str(plist.get("ProgramArguments"))).strip("[").strip("]")})
    if os.path.exists(progExecutable):
      parsedPlist.update({'hash':progExecutableHash})
      if (vtResultRequested):
        parsedPlist.update({'virustotal_result':progVTResult})
      parsedPlist.update({'executable':progExecutable})
      parsedPlist.update({"signing_info":checkSignature(progExecutable)})
    parsedPlist.update({'plist_hash':getHash(plist_file, True)})
    parsedPlist.update({'path':plist_file})
    return parsedPlist

def getLaunchAgents(path,output_file,ignoreVFlag):
    #get all of the launch agents at a specififc location returned into a list
    print("%s" % "[+] Gathering Launch Agent data.")
    launchAgents = os.listdir(path)
    #for each of the launchAgents, parse the contents into a dictionary, add the name of the plist and the location to the dictionary
    for agent in launchAgents:
      parsedAgent = {}
      parsedAgent = parseAgentsDaemons(agent,path)
      parsedAgent.update({"module":"launch_agents"})
      parsedAgent.update({"hostname":hostname})
      parsedAgent.update({"UUID":UUID})
      json.dump(parsedAgent,output_file)
      outfile.write("\n")

def getLaunchDaemons(path,output_file,ignoreVFlag):
    print("%s" % "[+] Gathering Launch Daemon data.")
    launchDaemons = os.listdir(path)
    #for each of the launchAgents, parse the contents into a dictionary, add the name of the plist and the location to the dictionary
    for daemon in launchDaemons:
      parsedDaemon = {}
      parsedDaemon = parseAgentsDaemons(daemon,path)
      parsedDaemon.update({"module":"launch_daemons"})
      parsedDaemon.update({"hostname":hostname})
      parsedDaemon.update({"UUID":UUID})
      json.dump(parsedDaemon,output_file)
      outfile.write("\n")

#get a list of users on the system
def getUsers(output_file):
    print("%s" % "[+] Gathering users on the system.")
    users_dict = {}
    all_users = []
    #run command to get a list of all the users
    users = subprocess.Popen(["dscl",".","list","/Users"], stdout=subprocess.PIPE).communicate()
    users = users[0].split("\n")
    #if the user is a normal system account, add to the all users array/list
    for user in users:
        if user.startswith('_') == False:
             all_users.append(user)
    users_dict.update({'users': all_users})
    users_dict.update({"module":"users"})
    users_dict.update({"hostname":hostname})
    users_dict.update({"UUID":UUID})
    json.dump(users_dict,output_file)
    outfile.write("\n")
    return users_dict

#get all the safari extensions on the system
def getSafariExtensions(path,output_file):
  print("%s" % "[+] Gathering Safari Extensions data.")
  extension = []
  plist_file = path+'/Extensions.plist'
  plist = Foundation.NSDictionary.dictionaryWithContentsOfFile_(plist_file)
  if plist:
    for ext in plist.get("Installed Extensions"):
      safariExtensions = {}
      safariExtensions.update({"module":"safari_extensions"})
      safariExtensions.update({'extension_name':ext.get("Archive File Name")})
      safariExtensions.update({'apple_signed':ext.get("Apple-signed")})
      safariExtensions.update({'developer_identifier':ext.get("Developer Identifier")})
      safariExtensions.update({'extension_path':plist_file})
      safariExtensions.update({"hostname":hostname})
      safariExtensions.update({"UUID":UUID})
      json.dump(safariExtensions,output_file)
      outfile.write("\n")

#get all chrome extensions on the system
def getChromeExtensions(path,output_file):
  print("%s" % "[+] Gathering Chrome Extensions data.")
  if os.path.exists(path):
    extensions_directories = os.listdir(path)
    for directory in extensions_directories:
      full_path = path+directory
      for root, dirs, files in os.walk(full_path, topdown=False):
        for name in files:
          if name == "manifest.json":
            with open(os.path.join(root,name),'r') as manifest:
              manifest_dump = manifest.read()
            manifest_json = json.loads(manifest_dump)
            for field in manifest_json:
              extensions = {}
              if field == "name":
                if manifest_json.get("name").startswith('__') == False:
                  extensions.update({"extension_directory_name":directory})
                  update_url = manifest_json.get("update_url")
                  if update_url:
                    extensions.update({"extension_update_url":update_url.strip('u\'')})
                  else:
                    extensions.update({"extension_update_url":"Null"})
                  extensions.update({"extension_name":manifest_json.get("name").strip('u\'')})
                  extensions.update({"module":"chrome_extensions"})
                  extensions.update({"hostname":hostname})
                  extensions.update({"UUID":UUID})
                  json.dump(extensions,output_file)
                  outfile.write("\n")

# get chrome downloads and visit history
def getChromeDownloads(chromeHistoryDbPath,output_file):
  print("%s" % "[+] Gathering Chrome Downloads history.")

  # database is locked
  _,historyCopyPath = tempfile.mkstemp()
  shutil.copy(chromeHistoryDbPath, historyCopyPath)
  try :
    db = sqlite3.connect(historyCopyPath)
    db.row_factory = sqlite3.Row
    c = db.cursor()
    results = c.execute("SELECT * FROM downloads ORDER BY start_time DESC").fetchall()
    chrome_epoch_start = datetime.datetime(1601,1,1)
    dangerTypeEnum = ("none", "file", "url", "content", "uncommon", "host", "unwanted", "safe", "accepted")
    statusEnum = ("in_progress", "interrupted", "complete")
    for row in results:
      download = dict((k, row[k]) for k in ("total_bytes", "opened","referrer", "by_ext_id", 
      "by_ext_name", "mime_type", "original_mime_type", "site_url", "tab_url", "tab_referrer_url"))
      start_time = chrome_epoch_start + datetime.timedelta(microseconds=int(row['start_time']))
      download.update({
        "module": "chrome_downloads",
        "hostname": hostname,
        "UUID": UUID,
        "start_time": start_time.isoformat() + 'Z',
        "target_path": row["target_path"].encode("utf-8"),
        "current_path": row["current_path"].encode("utf-8"),
        "hash": binascii.hexlify(row["hash"]),
        "danger_type": dangerTypeEnum[row["danger_type"]],
        "state": statusEnum[row["state"]]
      })
      
      json.dump(download,output_file)
      output_file.write("\n")
  except sqlite3.OperationalError:
    print("[-] Unable to connect to the chrome history database")
  except:
    print("[-] Error parsing chrome history database")
  finally:
    os.remove(historyCopyPath)
  



#get all firefox extensions on the system
def getFirefoxExtensions(path,output_file):
  print("%s" % "[+] Gathering Firefox Extensions data.")
  try:
    with open(path+"profiles.ini",'r') as profile_data:
      profile_dump = profile_data.read()
  except:
    return

  extensions_path = profile_dump[profile_dump.find("Path="):profile_dump.find("\\n")].split('\n')[0]
  extensions_path = extensions_path.split("=")[1]

  with open(path+extensions_path+"/extensions.json", 'r') as extensions:
    extensions_dump = extensions.read()
  extensions_json = json.loads(extensions_dump)

  for field in extensions_json.get("addons"):
    firefox_extensions = {}
    firefox_extensions.update({"extension_id": field.get("id")})
    firefox_extensions.update({"extension_update_url": field.get("updateURL")})
    firefox_extensions.update({"extension_options_url": field.get("optionsURL")})
    firefox_extensions.update({"extension_install_date": field.get("installDate")})
    firefox_extensions.update({"extension_last_updated": field.get("updateDate")})
    firefox_extensions.update({"extension_source_uri": field.get("sourceURI")})
    firefox_extensions.update({"extension_name": field.get("defaultLocale").get("name")})
    firefox_extensions.update({"extension_description": field.get("defaultLocale").get("description")})
    firefox_extensions.update({"extension_creator": field.get("defaultLocale").get("creator")})
    firefox_extensions.update({"extension_homepage_url": field.get("defaultLocale").get("homepageURL")})
    firefox_extensions.update({"module":"firefox_extensions"})
    firefox_extensions.update({"hostname":hostname})
    firefox_extensions.update({"UUID":UUID})
    json.dump(firefox_extensions,output_file)
    outfile.write("\n")

def getInstallHistory(output_file):
  print("%s" % "[+] Gathering Install History data.")
  path = '/Library/Receipts/InstallHistory.plist'
  history = plistlib.readPlist(path)
  for item in history:
    tempdict = item
    installList = {}
    installList.update({"install_date":tempdict.get('date')})
    installList.update({"display_name":tempdict.get('displayName')})
    installList.update({"package_identifier":tempdict.get('packageIdentifiers')})
    installList.update({"module":"install_history"})
    installList.update({"hostname":hostname})
    installList.update({"UUID":UUID})
    json.dump(installList,output_file,default=datetime_handler,encoding='latin1')
    output_file.write("\n")


def getCronJobs(users,output_file):
  #get all of the current users
  print("%s" % "[+] Gathering current cron jobs.")
  usercrons = {}
  for user in users:
    #results in a tuple
    users_crontab = subprocess.Popen(["crontab","-u",user,"-l"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    #add user and associated crontabs to dict usercrons
    usercrons.update({"user":user})
    usercrons.update({"crontab":users_crontab})
    usercrons.update({"module":"cron_jobs"})
    usercrons.update({"hostname":hostname})
    usercrons.update({"UUID":UUID})
    json.dump(usercrons,output_file)
    output_file.write("\n")

def getEmond(output_file):
  print("%s" % "[+] Gathering Emond Rules.")
  emondRules = []
  allRules = {}
  for root, dirs, files in os.walk('/etc/emond.d/rules/', topdown=False):
    for name in files:
      emondRules.append(os.path.join(root, name))
  for rule in emondRules:
    allRules.update({rule:plistlib.readPlist(rule)})
    allRules.update({"rule":rule})
    allRules.update({"module":"emond_rules"})
    allRules.update({"hostname":hostname})
    allRules.update({"UUID":UUID})
    json.dump(allRules,output_file)
    output_file.write("\n")

def getKext(sipStatus,kextPath,output_file,ignoreVFlag):
  print("%s" % "[+] Gathering Kernel Extensions data.")
  kexts = os.listdir(kextPath)
  for kext in kexts:
    for root, dirs, files in os.walk(kextPath+"/"+kext, topdown=False):
      for name in files:
        kextDict = {}
        if name == ("Info.plist"):
          try:
            kextPlist = plistlib.readPlist(os.path.join(root, name))
          except:
            kextDict.update({"Plist_parsing_error":"Unable to parse plist for "+kextPath})

          if (kextPlist):
            executable = kextPlist.get("CFBundleExecutable")
            if (executable):
              executable_path = kextPath+"/"+kext+"/Contents/MacOS/"+executable
            else:
              executable = "None or Parsing Error"
              executable_path = "None or Parsing Error"

            if os.path.exists(executable_path):
              kext_sig = checkSignature(executable_path,None)
              kext_hash, kext_vtResult = getHash(executable_path,ignoreVFlag)
            else:
              kext_sig = "Parsing Error"
              kext_hash = "Parsing Error"

            kextDict.update({"CFBundleName":kextPlist.get("CFBundleName")})
            kextDict.update({"CFBundleExecutable":executable})
            kextDict.update({"CFBundleExecutable_signature":kext_sig})
            kextDict.update({"CFBundleExecutable_hash":kext_hash})
            if vtResultRequested:
              kextDict.update({"virustotal_result":kext_vtResult})

            kextDict.update({"CFBundleIdentifier":kextPlist.get("CFBundleIdentifier")})
            kextDict.update({"OSBundleRequired":kextPlist.get("OSBundleRequired")})
            kextDict.update({"CFBundleGetInfoString":kextPlist.get("CFBundleGetInfoString")})

          kextDict.update({"kext_path":os.path.join(root, name)})
          kextDict.update({"module":"kernel_extensions"})
          kextDict.update({"hostname":hostname})
          kextDict.update({"UUID":UUID})
          json.dump(kextDict,output_file)
          output_file.write("\n")

def getEnv(output_file):
  print("%s" % "[+] Gathering Environment Variables.")
  envVars = subprocess.Popen(["env"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].split('\n')
  for var in envVars:
    env = {}
    envValue = var.split("=")
    if len(envValue) > 1 and envValue[0] != "VTKEY":
      env.update({envValue[0]:envValue[1]})
      env.update({"module":"environment_variables"})
      env.update({"hostname":hostname})
      env.update({"UUID":UUID})
      json.dump(env,output_file)
      output_file.write("\n")

def getPeriodicScripts(output_file):
  print("%s" % "[+] Gathering Periodic Scripts.")
  periodic = {}
  periodicDirs = ['/etc/periodic/daily/','/etc/periodic/weekly/','/etc/periodic/monthly/']
  for item in periodicDirs:
    periodicLst = []
    for root, dirs, files in os.walk(item, topdown=False):
      for name in files:
        periodicLst.append(name)
      periodic.update({item:periodicLst})
      periodic.update({"module":"periodic_scripts"})
      periodic.update({"hostname":hostname})
      periodic.update({"UUID":UUID})
      json.dump(periodic,output_file)
      output_file.write("\n")

def getConnections(output_file):
  print("%s" % "[+] Gathering current network connections.")
  #get process listing with connections
  processes = subprocess.Popen(["lsof","-i"], stdout=subprocess.PIPE).communicate()[0].split('\n')
  lstofprcs = []
  for process in processes:
    processList = process.split(" ")
    tmplist = []
    #if a process has an established connection dump the contents in a new list
    if '(ESTABLISHED)' in processList:
      for item in processList:
        if len(item) > 0:
          tmplist.append(item)
      lstofprcs.append(tmplist)
  for process in lstofprcs:
    connections= {}
    connections.update({"process_name":process[0]})
    connections.update({"process_id":process[1]})
    connections.update({"user":process[2]})
    connections.update({"TCP_UDP":process[7]})
    connections.update({"connection_flow":process[8]})
    connections.update({"module":"established_connections"})
    connections.update({"hostname":hostname})
    connections.update({"UUID":UUID})
    json.dump(connections,output_file)
    output_file.write("\n")

def SIPStatus(output_file):
  print("%s" % "[+] Gathering System Intergrity Protection status.")
  sip = {}
  status = subprocess.Popen(["csrutil","status"], stdout=subprocess.PIPE).communicate()[0]
  status = status.strip('\n').strip(".").split(":")[1].strip(" ")
  sip.update({"sip_status":status})
  sip.update({"module":"system_intergrity_protection"})
  sip.update({"hostname":hostname})
  sip.update({"UUID":UUID})
  json.dump(sip,output_file)
  outfile.write("\n")
  return sip


def GatekeeperStatus(output_file):
  print("%s" % "[+] Gathering Gatekeeper status.")
  gatekeeper = {}
  status = subprocess.Popen(["spctl","--status"], stdout=subprocess.PIPE).communicate()[0]
  gatekeeper.update({"gatekeeper_status":status})
  gatekeeper.update({"module":"gatekeeper_status"})
  gatekeeper.update({"hostname":hostname})
  gatekeeper.update({"UUID":UUID})
  json.dump(gatekeeper,output_file)
  outfile.write("\n")

def parseApp(app,ignoreVFlag):
  appInfo = {}
  appPlist = app+"/Contents/Info.plist"
  if os.path.exists(appPlist):
    plist_type = subprocess.Popen(["file", appPlist], stdout=subprocess.PIPE).communicate()
    plist_type = plist_type[0].split(":")[1].strip("\n").strip(" ")
    plist = None
    if plist_type == 'Apple binary property list':
      plist = Foundation.NSDictionary.dictionaryWithContentsOfFile_(appPlist)
    elif "XML 1.0 document text" in plist_type:
      plist = plistlib.readPlist(appPlist)
    else:
      appInfo.update({"application":app})
      return appInfo

    executable = plist.get("CFBundleExecutable")
    executable_path = app+"/Contents/MacOS/"+executable

    if os.path.exists(executable_path):
      app_sig = checkSignature(executable_path,None)
      app_hash, app_ktResult = getHash(executable_path,ignoreVFlag)
    else:
      app_sig = "Parsing Error"
      app_hash = "Parsing Error"

    appInfo.update({"application":app})
    appInfo.update({"executable":executable})
    appInfo.update({"executable_path":executable_path})
    appInfo.update({"application_hash":app_hash})
    if vtResultRequested:
      appInfo.update({"virustotal_result": app_ktResult})
    appInfo.update({"signature":app_sig})
  return appInfo

def getLoginItems(path,output_file,ignoreVFlag):
  print("%s" % "[+] Gathering Login Items for each user.")
  #Parsing - Library/Application\ Support/com.apple.backgroundtaskmanagementagent/backgrounditems.btm
  plist_file = path
  loginApps = []
  plist = Foundation.NSDictionary.dictionaryWithContentsOfFile_(plist_file)
  objects = plist.get("$objects")
  for item in objects:
    if item.isKindOfClass_(Foundation.NSClassFromString("NSData")) == True:
      bookmark = item
      properties = Foundation.NSURL.resourceValuesForKeys_fromBookmarkData_(['NSURLBookmarkAllPropertiesKey'],bookmark)
      loginApps.append(properties.get("NSURLBookmarkAllPropertiesKey").get("_NSURLPathKey"))
    elif item.isKindOfClass_(Foundation.NSClassFromString("NSDictionary")) == True:
      if item.has_key("NS.data"):
        bookmark = item.get("NS.data")
        properties = Foundation.NSURL.resourceValuesForKeys_fromBookmarkData_(['NSURLBookmarkAllPropertiesKey'],bookmark)
        loginApps.append(properties.get("NSURLBookmarkAllPropertiesKey").get("_NSURLPathKey"))
  loginApps = set(loginApps)
  loginApps = list(loginApps)
  for item in loginApps:
    loginItems = {}
    #if there are apps in Login Items, parse them.
    if item:
      loginItems = parseApp(item,ignoreVT)
      loginItems.update({"module":"login_items"})
      loginItems.update({"hostname":hostname})
      loginItems.update({"UUID":UUID})
      json.dump(loginItems,output_file)
      outfile.write("\n")

def getApps(path,output_file,ignoreVFlag):
  print("%s" % "[+] Gathering Applications for each user.")
  if vtResultRequested:
    print("%s" % "[++] Querying VirusTotal as we go.")

  app_lst = os.listdir(path)
  for app in app_lst:
    apps = {}
    app = path+"/"+app
    try:
      apps = parseApp(app,ignoreVT)
    except:
      apps.update({"app error":"issue parsing application information for app"+str(app)})
      continue

    apps.update({"module":"applications"})
    apps.update({"hostname":hostname})
    apps.update({"UUID":UUID})
    json.dump(apps,output_file)
    outfile.write("\n")



def getEventTaps(output_file):
  print("%s" % "[+] Gathering installed Event Taps.")
  evInfo = Quartz.CGGetEventTapList(10,None,None)
  for item in evInfo[1]:
    eventTap = {}
    eTap = str(item).strip("<").strip(">").split(" ")
    tappingProcess = eTap[5].split("=")[1]
    tappedProcess = eTap[6].split("=")[1]
    tappingProcName = subprocess.Popen(["ps", "-p", tappingProcess, "-o", "comm="], stdout=subprocess.PIPE).communicate()[0]
    eventTap.update({"eventTapID":eTap[1].split("=")[1]})
    eventTap.update({"hostname":hostname})
    eventTap.update({"UUID":UUID})
    eventTap.update({"tapping_process_id":tappingProcess})
    eventTap.update({"tapping_process_name":tappingProcName})
    eventTap.update({"tapped_process_id":tappedProcess})
    eventTap.update({"enabled":eTap[7].split("=")[1]})
    eventTap.update({"module":"event_taps"})
    json.dump(eventTap,output_file)
    outfile.write("\n")

def getBashHistory(output_file, users):
  print("%s" % "[+] Gathering Bash History data.")
  userBashHistory = {}
  for user in users:
    history_file = '/Users/'+user+'/.bash_history'
    if os.path.isfile(history_file):
      with open(history_file, 'r') as bash_history:
        history_data = bash_history.read()
      history_data = history_data.split('\n')
      userBashHistory.update({"user":user})
      userBashHistory.update({"hostname":hostname})
      userBashHistory.update({"UUID":UUID})
      userBashHistory.update({"bash_commands":history_data})
      userBashHistory.update({"module":"bash_history"})
      json.dump(userBashHistory,output_file)
      outfile.write("\n")

def getShellStartupScripts(users, output_file):
  # Get any user profile scripts. These scripts are run every time a shell is launched by a user.
  # A malicious actor can add a backdoor script into these files, then either wait for the
  # user to logon, or launch a shell using an innocuous cronjob, etc.
  print("[+] Gathering any shell startup scripts ('~/.bash_profile', etc.)")
  startup_files = [
    "/Users/%s/.bash_profile",  # This is the typical one that exists on OSX
    "/Users/%s/.bashrc",        # This is the linux standard, but may still exist
    "/Users/%s/.profile"        # Mac OS X Yosemite might have this one according to SO
  ]
  for user in users:
    for startup_file in startup_files:
      startup_filename = startup_file % users
      if os.path.isfile(startup_filename):
        with open(startup_filename, "r") as f:
          startup_data = f.read().split('\n')

        # Add to output file
        users_script = {
          "user": user,
          "hostname": hostname,
          "UUID": UUID,
          "module": "shell_startup",
          "shell_startup_filename": startup_filename,
          "shell_startup_data": startup_data
        }
        json.dump(users_script,output_file, sort_keys=True)
        output_file.write("\n")


#
# AWS UPLOAD (without requests module)
#

AMZN_SIGNED_HEADERS = ['content-md5', 'content-type',
                       'host', 'x-amz-content-sha256',
                       'x-amz-date']
AMZN_CONTENT_SHA256 = 'UNSIGNED-PAYLOAD'


def hmac_sha256(key, data):
    return hmac.new(key, data, hashlib.sha256).digest()


def amzn_sig(secret_access_key, data, aws_region, aws_service='s3'):
    today = datetime.datetime.utcnow().strftime('%Y%m%d')
    date_key = hmac_sha256('AWS4' + secret_access_key, today)
    date_region_key = hmac_sha256(date_key, aws_region)
    date_region_svc_key = hmac_sha256(date_region_key, aws_service)
    sign_key = hmac_sha256(date_region_svc_key, 'aws4_request')

    return hmac.new(sign_key, data, hashlib.sha256).hexdigest()


def amzn_canonical_req(filename_path, headers_list):
    headers = dict([(k.lower(), v.strip()) for k, v in headers_list])
    canonical_hdrs = []
    for amzn_header in AMZN_SIGNED_HEADERS:
        canonical_hdrs.append('{}:{}'.format(
            amzn_header, headers[amzn_header]))
    return 'PUT\n{}\n\n{}\n\n{}\n{}'.format(filename_path,
                                            '\n'.join(canonical_hdrs),
                                            ';'.join(AMZN_SIGNED_HEADERS),
                                            AMZN_CONTENT_SHA256)


def s3_upload(data, content_type, filename_path, access_key_id, secret_access_key, s3_bucket, aws_region):
    s3_host = '{}.s3.{}.amazonaws.com'.format(s3_bucket, aws_region)
    if not filename_path.startswith('/'):
        filename_path = '/' + filename_path
    s3_upload_url = 'https://{}{}'.format(s3_host, filename_path)

    put_req = urllib2.Request(s3_upload_url, data=data)
    put_req.get_method = lambda: 'PUT'

    now = datetime.datetime.utcnow()
    amzn_ts = now.strftime('%Y%m%dT%H%M%SZ')
    amzn_date = now.strftime('%Y%m%d')

    data_md5 = base64.b64encode(hashlib.md5(data).digest())
    put_req.add_header('Host', s3_host)
    put_req.add_header('Content-MD5', data_md5)
    put_req.add_header('X-Amz-Date', amzn_ts)
    put_req.add_header('Content-Type', content_type)  # 'application/zip')
    put_req.add_header('X-Amz-Content-SHA256', AMZN_CONTENT_SHA256)

    # canonical request to build signature
    canonical_req = amzn_canonical_req(filename_path, put_req.header_items())
    scope = '{}/{}/s3/aws4_request'.format(amzn_date, aws_region)
    hash_canonical_req = hashlib.sha256(canonical_req).hexdigest()
    to_sign = 'AWS4-HMAC-SHA256\n{}\n{}\n{}'.format(
        amzn_ts,
        scope,
        hash_canonical_req)
    req_sig = amzn_sig(secret_access_key, to_sign, aws_region)

    # build Authorization header
    signed_headers = ';'.join(AMZN_SIGNED_HEADERS)
    creds = '{}/{}'.format(access_key_id, scope)
    auth_header = 'AWS4-HMAC-SHA256 Credential={}, SignedHeaders={}, Signature={}'.format(
        creds, signed_headers, req_sig)
    put_req.add_header('Authorization', auth_header)

    # upload file or die
    opener = urllib2.build_opener(urllib2.HTTPHandler())
    try:
        conn = opener.open(put_req)
    except urllib2.HTTPError as e:
        return False

    return conn.code == 200

if __name__ == '__main__':
  script_start = time.time()
  output_list = []
  output = {}
  sipStatus = True

  outputFile = hostname
  outputDirectory = os.getcwd()
  print("%s" % """
__     __               _
\ \   / /__ _ __   __ _| |_ ___  _ __
 \ \ / / _ \ '_ \ / _` | __/ _ \| '__|
  \ V /  __/ | | | (_| | || (_) | |
   \_/ \___|_| |_|\__,_|\__\___/|_|
          """)



  parser = argparse.ArgumentParser(description='Helpful information for running your macOS Hunting Script.')
  parser.add_argument('-f',metavar='File Name',default=outputFile, help='Name of your output file (by default the name is the hostname of the system).')
  parser.add_argument('-d', metavar='Directory',default=outputDirectory, help='Directory of your output file (by default it is the current working directory).')
  parser.add_argument('-a', metavar='<BUCKET_NAME>:<AWS_KEY_ID>:<AWS_KEY_SECRET>:<AWS_REGION>', help='Your AWS Key if you want to upload to S3 bucket.')
  parser.add_argument('-v',  action="store_true",dest="vtResultRequested", help='If present, hashes will be sent to VirusTotal for checking (severely slows down performance)')
  args = parser.parse_args()
  
  outputFilename = args.f + '.json'
  outputPath = os.path.join(args.d, outputFilename)

  if args.vtResultRequested:
    vtResultRequested = True
    ignoreVT = False
    vtAPIKey = os.getenv("VTKEY")
    if vtAPIKey is None:
      print("You asked for results from VirusTotal but did not put an API key in the variable VTKEY")
      sys.exit(-1)
  else:
    ignoreVT = True



  outputPath = args.d+"/"+args.f+".json"

  if not os.geteuid()==0:
    sys.exit('This script must be run as root!')

  with open(outputPath, 'w') as outfile:

    lst_of_users = getUsers(outfile).get("users")
    sipEnabled = SIPStatus(outfile).get("sip_status")


    modules = [getSystemInfo(outfile),getInstallHistory(outfile),GatekeeperStatus(outfile),getConnections(outfile),
    getEnv(outfile),getPeriodicScripts(outfile), getCronJobs(lst_of_users,outfile),getEmond(outfile),getLaunchAgents('/Library/LaunchAgents',outfile,ignoreVT),getShellStartupScripts(lst_of_users,outfile),
    getLaunchDaemons('/Library/LaunchDaemons',outfile,ignoreVT),getKext(sipStatus,'/Library/Extensions',outfile,ignoreVT),getApps('/Applications',outfile,ignoreVT),getEventTaps(outfile),getBashHistory(outfile,lst_of_users)]

    for module in modules:
      module

    #user specific modules
    for user in lst_of_users:
      userLaunchAgent = '/Users/'+user+'/Library/LaunchAgents'
      chromeEx = '/Users/'+user+'/Library/Application Support/Google/Chrome/Default/Extensions/'
      chromeHistory = '/Users/'+user+'/Library/Application Support/Google/Chrome/Default/History'
      firefoxEx = '/Users/'+user+'/Library/Application Support/Firefox/'
      safariEx = '/Users/'+user+'/Library/Safari/Extensions'
      loginItemDir = '/Users/'+user+'/Library/Application Support/com.apple.backgroundtaskmanagementagent/backgrounditems.btm'
      apps_dir = '/Users/'+user+'/Applications'

      if os.path.exists(userLaunchAgent):
        getLaunchAgents(userLaunchAgent,outfile,ignoreVT)
      if os.path.exists(chromeEx):
        getChromeExtensions(chromeEx,outfile)
      if os.path.exists(chromeHistory):
        getChromeDownloads(chromeHistory,outfile)
      if os.path.exists(firefoxEx):
        getFirefoxExtensions(firefoxEx,outfile)
      if os.path.exists(safariEx):
        getSafariExtensions(safariEx,outfile)
      if os.path.exists(loginItemDir):
        getLoginItems(loginItemDir,outfile,ignoreVT)
      if os.path.exists(apps_dir):
        getApps(apps_dir,outfile,ignoreVT)

    if (sipEnabled != 'enabled'):
      sipStatus = False

    #if SIP is disabled, check for items in /System directory
    if sipStatus == False:
      print("%s" % "[!!!!!] System Integrity Protection is disabled. Gathering additional data launch agent/daemon data.")
      output_list.append(getLaunchAgents('/System/Library/LaunchAgents',outfile))
      output_list.append(getLaunchDaemons('/System/Library/LaunchDaemons',outfile,ignoreVT))
      output_list.append(getKext(sipStatus,'/System/Library/Extensions',outfile,ignoreVT))

    #time.sleep(60)
    records_count = len(open(outputPath).readlines(  ))

    if args.a:
      bucket_name, aws_key, aws_secret, aws_region = args.a.split(':')
      with open(outputPath, 'r') as oh:
        didUpload = s3_upload(oh.read(), 'application/json', '/uploads/' + outputFilename,
              aws_key, aws_secret, bucket_name, aws_region)
        if didUpload == True:
          print("[+] results uploaded to S3 (%s)" % outputFilename)
          try:
            os.remove(outputPath)
          except:
            pass
        else:
          print("[+] results were not uploaded to S3 (%s)" % outputFilename)
      
      

    script_end = time.time()
    total_time = script_end - script_start

    print("[***] Venator collection completed in %s seconds. Location of your output file:%s" %  (str(total_time),outputPath))
    print("[***] Venator collection completed in %s seconds with %s records. Location of your output file:%s" %  (str(total_time),str(records_count),outputPath))
