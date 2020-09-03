"""
# pypipelist

                      _            _ _     _
                     (_)          | (_)   | |
    _ __  _   _ _ __  _ _ __   ___| |_ ___| |_
   | '_ \| | | | '_ \| | '_ \ / _ | | / __| __|
   | |_) | |_| | |_) | | |_) |  __| | \__ | |_
   | .__/ \__, | .__/|_| .__/ \___|_|_|___/\__|
   | |     __/ | |     | |
   |_|    |___/|_|     |_|


## About
This tool performs the same actions as SysInternal's pipelist but performs additional queries to
provide a lot more useful information.

This tool is noisy (see getpipeperms()). It's designed for research not stealth.

This is work in progress... needs a fair bit of TLC.

TODO:
This tool should be able to support mailslots.

Refs:
http://timgolden.me.uk/pywin32-docs/win32pipe.html
https://docs.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-getnamedpipeinfo

Example usage:
(pipes) C:\Users\admin\Documents\pipes>python pypipelist.py
InitShutdown                                 Perms.R   proc=wininit.exe:528                                                          PipeFlags.TYPE_MESSAGE   readbuf=2048   writebuf=2048   maxinstances=255
InitShutdown                                 Perms.W   proc=wininit.exe:528                                                          PipeFlags.TYPE_MESSAGE   readbuf=2048   writebuf=2048   maxinstances=255
lsass                                        Perms.R   proc=lsass.exe:684                                                            PipeFlags.TYPE_MESSAGE   readbuf=2048   writebuf=2048   maxinstances=255
lsass                                        Perms.W   proc=lsass.exe:684                                                            PipeFlags.TYPE_MESSAGE   readbuf=2048   writebuf=2048   maxinstances=255
ntsvcs                                       Perms.R   proc=services.exe:660                                                         PipeFlags.TYPE_MESSAGE   readbuf=2048   writebuf=2048   maxinstances=255
ntsvcs                                       Perms.W   proc=services.exe:660                                                         PipeFlags.TYPE_MESSAGE   readbuf=2048   writebuf=2048   maxinstances=255
scerpc                                       Perms.R   proc=services.exe:660                                                         PipeFlags.TYPE_MESSAGE   readbuf=2048   writebuf=2048   maxinstances=255
scerpc                                       Perms.W   proc=services.exe:660                                                         PipeFlags.TYPE_MESSAGE   readbuf=2048   writebuf=2048   maxinstances=255
Winsock2\CatalogChangeListener-3b8-0         Perms.R   code (5, 'CreateFile', 'Access is denied.')
Winsock2\CatalogChangeListener-3b8-0         Perms.W   code (5, 'CreateFile', 'Access is denied.')
epmapper                                     Perms.R   proc=svchost.exe:952                                                          PipeFlags.TYPE_MESSAGE   readbuf=2048   writebuf=2048   maxinstances=255
epmapper                                     Perms.W   proc=svchost.exe:952                                                          PipeFlags.TYPE_MESSAGE   readbuf=2048   writebuf=2048   maxinstances=255
Winsock2\CatalogChangeListener-210-0         Perms.R   code (5, 'CreateFile', 'Access is denied.')
Winsock2\CatalogChangeListener-210-0         Perms.W   code (5, 'CreateFile', 'Access is denied.')
LSM_API_service                              Perms.R   proc=svchost.exe:816                                                          PipeFlags.TYPE_MESSAGE   readbuf=2048   writebuf=2048   maxinstances=255
LSM_API_service                              Perms.W   proc=svchost.exe:816                                                          PipeFlags.TYPE_MESSAGE   readbuf=2048   writebuf=2048   maxinstances=255
atsvc                                        Perms.R   proc=svchost.exe:1108                                                         PipeFlags.TYPE_MESSAGE   readbuf=2048   writebuf=2048   maxinstances=255
atsvc                                        Perms.W   proc=svchost.exe:1108                                                         PipeFlags.TYPE_MESSAGE   readbuf=2048   writebuf=2048   maxinstances=255
eventlog                                     Perms.R   proc=svchost.exe:1236                                                         PipeFlags.TYPE_MESSAGE   readbuf=2048   writebuf=2048   maxinstances=255
eventlog                                     Perms.W   proc=svchost.exe:1236                                                         PipeFlags.TYPE_MESSAGE   readbuf=2048   writebuf=2048   maxinstances=255
...SNIPPED...

DK @withdk
https://github.com/withdk
August 2020

## Disclaimer
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import win32 as w32
import win32pipe as w32pipe
import win32file as w32file
import pywintypes
import win32con as w32con # contains win32 constants
from enum import Enum
import os
import time
import wmi

class Perms(Enum):
    R = w32con.GENERIC_READ
    W = w32con.GENERIC_WRITE

class PipeFlags(Enum):
    TYPE_BYTE = w32con.PIPE_TYPE_BYTE
    TYPE_MESSAGE = w32con.PIPE_TYPE_MESSAGE

def getnamedpipes():
    """ Available pipes are accessible via a standard file list call """
    return(os.listdir("\\\\.\\pipe\\"))

def printpipes(pipeslist):
    """ Loop over pipes to perform further queries """
    for p in pipeslist:
        getpipeperms(p)

def getpipeperms(pipename):
    """ Enumerate pipe permissions via CreateFile. This is NOISY! """
    fullpipename = "\\\\.\\pipe\\" + pipename
    for perm in Perms:
        phandle = getpipehandle(pipename, fullpipename, perm.value)
        if(phandle != -1):
            (flag, readbuf, writebuf, instances) = getnamedpipeinfo(phandle)
            svrpid = getnamedpipesvrpid(phandle)
            svrprocname = getprocbypid(wmiobj,svrpid)
            prettyflag = getprettyflag(flag)
            print(f"{pipename:<45}{getprettyperms(perm.value):<10}proc={svrprocname:<8}:{svrpid:<45}\
                {prettyflag:<25}readbuf={readbuf:<7}writebuf={writebuf:<7}maxinstances={instances}")
            phandle.close()
            #print(f"phandle = {phandle}")
        #time.sleep(0.2)

def getpipehandle(pipename, fullpipename, perms):
    """ returns a handle to pipename with requested perms
        @pipename: "\\\\.\\pipe\\name"
        @perms: GENERIC_READ, GENERIC_WRITE or GENERIC_READ | GENERIC_WRITE
    """
    try:
        phandle = w32file.CreateFile(fullpipename, perms, 0, None, w32file.OPEN_EXISTING, \
            w32file.FILE_ATTRIBUTE_NORMAL, None)
        if phandle == 0:
            print(f"Error connecting to pipe {pipename} code {phandle} ")
        else:
            return(phandle)
    except pywintypes.error as e:
        if e.args[0] == 2:
            print("No named pipe by that name")
        else:
            #verbose
            print(f"{pipename:<45}{getprettyperms(perms):<10}code {e}")
            pass
    return(-1)

def getnamedpipeinfo(phandle):
    """ returns pipe's flags, buffer sizes, and max instances
        @return (int, int, int, int)
    """
    return(w32pipe.GetNamedPipeInfo(phandle))

def getnamedpipesvrpid(phandle):
    """ returns pipe server process id
        @return (int)
    """
    return(w32pipe.GetNamedPipeServerProcessId(phandle))

def getprocnames():
    """ Gets a list of processes via WMI """
    w = wmi.WMI()
    return(w.Win32_Process())

def getprocbypid(wmiobj, pid):
    """ Queries WMI to convert PID to procnames """
    for p in wmiobj:
        if(pid==p.ProcessId):
            return(p.Name)
    return("Unknown")

def getprettyperms(perms):
    """ Helper function to pretty up output """
    for p in Perms:
        if(p.value == perms):
            return(p)
    return("?")

def getprettyflag(flag):
    """ Helper function to pretty up output """
    for f in PipeFlags:
        if(f.value == flag):
            return(f)
    return("?")

def main():
    global wmiobj

    wmiobj = getprocnames()
    pipeslist = getnamedpipes()
    printpipes(pipeslist)

if __name__ == "__main__":
    main()
