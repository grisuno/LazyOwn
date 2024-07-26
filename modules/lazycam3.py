#!/usr/bin/env python
#    This code is a portion of frigate Event Video Recorder (fEVR)
#
#    Copyright (C) 2021-2022  The Bearded Tek (http://www.beardedtek.com) William Kenny
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU AfferoGeneral Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#    Scans given ports of an IPv4 Address or an IPv4 Network for RTSP Streams and
#    adds them to or removes them from rtsp-simple-server via its API


from os import getenv,path,system
import subprocess
import requests
import json
from PIL import Image
from portscan import PortScan
    
class RTSPScanner:
    def __init__(self,verbose=False,wspace="-"):
        # GET ENVIRONMENT VARIABLES
        self.ports = getenv("RTSP_SCAN_PORTS","554,8554")
        self.timeout=getenv("FFMPEG_TIMEOUT",10)
        self.retries=getenv("FFMPEG_RETRIES",2)
        self.apiaddress = getenv("RTSP_SS_ADDRESS","192.168.2.240")
        self.apiport = getenv("RTSP_SS_PORT","9997")
        self.apitransport = getenv("RTSP_SS_TRANSPORT","http")
        self.mode = getenv("RTSP_MODE").lower() if getenv("RTSP_MODE") else "scan"
        self.verbose = True if verbose or str(getenv("RTSP_VERBOSE","false")).lower() == "true" else False
        self.whitespace = getenv("RTSP_WHITESPACE") if getenv("RTSP_WHITESPACE") else wspace
        self.creds = self.splitCSV(getenv("RTSP_CREDS","none"))
        self.paths = self.splitCSV(getenv("RTSP_PATHS","/Streaming/Channels/101,/live,live2"))
        self.address = getenv("RTSP_ADDRESS","192.168.2.0/24")
        self.cameras = []
            
    def run(self):
        self.scanner()
        if self.mode == "rem":
            self.delCameras()
        elif self.mode == "add":
            if self.verbose:
                print(f"Cameras Found: {self.cameras}")
                print(f"Creds Used: {self.creds}")
                print(f"Paths: {self.paths}")
                print(f"Scanned Address(es): {self.address}")
                print(f"Scanned Ports: {self.ports}")
            self.addCameras()
        else:
            for c in range(0,len(self.cameras)):
                self.cameras[c][0] = self.cameras[c][0].replace('.',self.whitespace)
            
        if not self.mode != "add":
            return self.cameras

    def resizeImg(self,img,output,height=180,ratio=1.777777778,fmt="webp"):
        if path.exists(img):
            # Resizes an image from the filesystem
            if path.exists(img):
                Image.open(img).resize((int(height*ratio),height)).save(output,fmt, quality=100,optimize=True)
                return "OK"
            else:
                return "resizeImg(): Image Path Does Not Exist"

    def splitCSV(self,csv):
        values = []
        for value in csv.split(','):
            values.append(value)
        return values

    def scanner(self):
        self.portscan = PortScan(self.address,self.ports)
        results = self.portscan.run()
        with self.portscan.q.mutex:
            unfinished = self.portscan.q.unfinished_tasks - len(self.portscan.q.queue)
            if unfinished <= 0:
                if unfinished < 0:
                    raise ValueError('task_done() called too many times')
                self.portscan.q.unfinished_tasks = unfinished
                self.portscan.q.queue.clear()
                self.portscan.q.not_full.notify_all()
        #if self.verbose:
            #print(results)
        for result in results:
            if result:
                for path in self.paths:
                    for cred in self.creds:
                        transport = f"rtsp://{cred}@" if cred != "none" else "rtsp://"
                        rtsp = f'{transport}{result[0]}:{result[1]}{path}'
                        status = f"Checking {rtsp}... "
                        if self.verbose:
                            print(status)
                        snapshot = f"/tmp/test.png"
                        thumbnail = f"/tmp/test.webp"
                        flaky = []
                        command = ['ffmpeg', '-y', '-frames', '1', snapshot, '-rtsp_transport', 'tcp', '-i', rtsp]
                        for x in range(0,self.retries):
                            try:
                                cmd = subprocess.run(command,stderr=subprocess.DEVNULL,timeout=self.timeout)
                                break
                            except subprocess.TimeoutExpired as e:
                                if self.verbose:
                                    label = f"Retry # {x}" if x > 0 else "1st Attempt"
                                    print(f"{label}: {e}")
                                timedout = True
                        if self.verbose:
                            print(f"Return Code: {cmd.returncode}")
                        if 'timedout' in locals():
                            if timedout:
                                flaky.append([str(result['ip']),rtsp])
                        if 'cmd' in locals() and cmd.returncode == 0:
                            self.cameras.append([str(result['ip']),rtsp])
                            status = "RTSP "
                            #resizeImg(self,img,output,height=180,ratio=1.777777778,fmt="webp"):
                            resize = self.resizeImg(snapshot,thumbnail)
                            if resize == "OK":
                                status += "VALID IMAGE"
                            else:
                                status += "NO IMAGE"
                        if self.verbose:
                            print(status)
        self.scanResults = {"cameras":self.cameras,"flaky":flaky,"portscan":results}

    def delCameras(self):
        for cam in range(0,len(self.cameras)):
            self.cameras[cam][0] = self.cameras[cam][0].replace(".",self.whitespace).replace(" ","_")
            apiURL = f'{self.apitransport}://{self.apiaddress}:{self.apiport}/v1/config/paths/remove/{self.cameras[cam][0]}'
            outputString = f"Deleting {self.cameras[cam][0]} - {self.cameras[cam][1]} | "
            response = requests.post(apiURL)
            outputCode = f"{response.status_code} : "
            if response.status_code == 200:
                outputResult = "SUCCESS"
            else:
                outputResult = "FAILURE"
            print(f"{outputString}{outputCode}{outputResult}")

    def addCameras(self):
        for cam in range(0,len(self.cameras)):
            jsonPostData =  {
                            "source": self.cameras[cam][1],
                            "sourceProtocol": "automatic",
                            "sourceAnyPortEnable": False,
                            "sourceFingerprint": "",
                            "sourceOnDemand": False,
                            "sourceOnDemandStartTimeout": "10s",
                            "sourceOnDemandCloseAfter": "10s",
                            "sourceRedirect": "",
                            "disablePublisherOverride": False,
                            "fallback": "",
                            "publishUser": "",
                            "publishPass": "",
                            "publishIPs": [],
                            "readUser": "",
                            "readPass": "",
                            "readIPs": [],
                            "runOnInit": "",
                            "runOnInitRestart": False,
                            "runOnDemand": "",
                            "runOnDemandRestart": False,
                            "runOnDemandStartTimeout": "10s",
                            "runOnDemandCloseAfter": "10s",
                            "runOnReady": "python3 /app/rtsp_event.py $RTSP_PATH READY",
                            "runOnReadyRestart": False,
                            "runOnRead": "python3 /app/rtsp_event.py $RTSP_PATH READ",
                            "runOnReadRestart": False
                            }
            cameraName = self.cameras[cam][0].replace(".",self.whitespace).replace(" ","-")
            outputString = f"Adding {self.cameras[cam][0]} - {self.cameras[cam][1]} | "
            outputCode = ""
            outputResult = ""
            apiHost = f'{self.apitransport}://{self.apiaddress}:{self.apiport}'
            apiURL = f'{apiHost}/v1/config/paths/add/{cameraName}'
            if self.mode == "add":
                try:
                    response = requests.post(apiURL,json=jsonPostData)
                except requests.ConnectionError as e:
                    print()
                    if self.verbose:
                        print(e)
                        print()
                    print(f"Cannot reach rtsp-simple-server at {apiHost}.")
                    print(f"Possible Causes: API not enabled")
                    print(f"                 transport (http/https) not correct: {self.apitransport}")
                    print(f"                 ip/fqdn not correct: {self.apiaddress}")
                    print(f"                 port number not correct: {self.apiport}")
                    return
                outputCode = f"{response.status_code} : "
                if response.status_code == 200:
                    outputResult = "SUCCESS"
                else:
                    outputResult = "FAILURE"
            else:
                outputResult = "DISABLED"
            print(f"{outputString}{outputCode}{outputResult}")
            if self.verbose and outputResult != "SUCCESS":
                print(json.dumps(jsonPostData,indent=2,sort_keys=True,ensure_ascii=True))

if __name__ == "__main__":

    def cla():
        # Import argparse here in case we don't want to use it...
        import argparse
        parser = argparse.ArgumentParser(description="Scans given ports of an IPv4 Address or an IPv4 Network for RTSP streams and adds them to rtsp-simple-server")
        parser.add_argument('-w','--whitespace',type=str,required=False,default='-',
                            help="Whitespace Replacement can be - _ or #")
        parser.add_argument('-a','--address',type=str,required=False,default='192.168.2.0/24',
                            help="Single ipv4 address or ipv4 network in CIDR notation ex: 192.168.0.100 or 192.168.0/24")
        
        parser.add_argument('-n','--name',required=False,default=None,
                            help="Camera Name | only used if single address given")
        
        parser.add_argument('-p','--ports',type=str,required=False,default='554,8554',
                            help="csv format: 554,8554")
        
        parser.add_argument('-pp','--paths',type=str,required=False,default="/Streaming/Channels/101,/live,/live2",
                            help="csv format: '/Streaming/Channels/101,/live,/live2'")
        
        parser.add_argument('-c','--creds',required=False,default="none",
                            help="csv formatted user:password pairs: username:password,user:pass")
        
        parser.add_argument('-m','--mode',type=str,required=True,
                            help="add - add cameras found / rem - remove cameras found")
        
        parser.add_argument('-A','--apiaddr',type=str,required=False,default="192.168.0.100",
                            help="rtsp-simple-server API IP Address/FQDN")
        
        parser.add_argument('-P','--apiport',type=str,required=False,default="9997",
                            help="rtsp-simple-server API Port")
        
        parser.add_argument('-t','--apitransport',type=str,required=False,default="http",
                            help='rtsp-simple-server API transport (http/https)')
        
        parser.add_argument('-T','--timeout',type=int,required=False,default=10,
                            help="Timeout for ffmpeg command to determine if rtsp stream exists")
        
        parser.add_argument('-R','--timeoutretries',type=int,required=False,default=3,
                            help="Number of retries on timeout for ffmpeg command to determine if rtsp stream exists")
        
        parser.add_argument('-v','--verbose',action='store_true',default=False,
                            help="Set verbosity to true")
        
        args = parser.parse_args()
        return args

    def main():
        system('stty sane')
        args = vars(cla())
        #print(args)
        scanner = RTSPScanner()
        scanner.address = args['address']
        scanner.ports = args['ports']
        scanner.verbose = args['verbose']
        scanner.whitespace = args['whitespace']
        scanner.creds = scanner.splitCSV(args['creds'])
        scanner.paths = scanner.splitCSV(args['paths'])
        scanner.apiaddress = args['apiaddr']
        scanner.apiport = args['apiport']
        scanner.apitransport = args['apitransport']
        scanner.timeout = args['timeout']
        scanner.retries = args['timeoutretries']
        args['mode'] = args['mode'].lower()
        if args['mode'] == "rem" or args['mode'] == "add":
            scanner.mode = args['mode']
            scanner.run()
        elif args['mode'] == "scan":
            scanner.scanner()
        else:
            print("\nInvalid Mode")
            print("  Valid modes are 'add' 'rem' 'scan'.\n")
            return
        # Print Results of the Port Scan
        sourcesCount = 0
        sources = ""
        for item in scanner.scanResults['portscan']:
            if item:
                sourcesCount += 1
                if item[0] == 'open':
                    sources += f"  {item['ip']}:{item['port']}\n"
        sourcesDisp = "Sources" if sourcesCount > 1 else "Source"
        output = f"\n{sourcesCount} Potential RTSP {sourcesDisp}:\n" + sources
        print(output)

        # Print Results of the RTSP Scan

        # Cameras Found
        cameraCount = len(scanner.scanResults['cameras'])
        CamDisp = "Cameras" if cameraCount > 1 else "Camera"
        print(f"{cameraCount} {CamDisp} Found:")
        for camera in scanner.scanResults['cameras']:
            print(f"  {camera[0]}: {camera[1]}")

        # Flaky Cameras Found
        flakyCount = len(scanner.scanResults['flaky'])
        if flakyCount > 0:
            CamDisp = "Cameras" if flakyCount > 1 else "Camera"
            print(f"\n{len(scanner.scanResults['flaky'])} Flaky {CamDisp}:")
            print(f"Potential {CamDisp.lower()} that cannot be verfied within {scanner.timeout} second timeout.")
            print("This can be increased using the command line option -t <seconds>")
            for camera in scanner.scanResults['flaky']:
                print(f"  {camera[0]}: {camera[1]}")

        # Credentials Used
        print(f"\nCredentials Used:")
        for cred in scanner.creds:
            print(f"  {cred}")

        #Paths Used
        print(f"\nPaths Used:")
        for path in scanner.paths:
            print(f"  {path}")
        system('stty sane')
        
    main()
    