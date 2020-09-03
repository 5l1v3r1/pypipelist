# pypipelist
```
                      _            _ _     _
                     (_)          | (_)   | |
    _ __  _   _ _ __  _ _ __   ___| |_ ___| |_
   | '_ \| | | | '_ \| | '_ \ / _ | | / __| __|
   | |_) | |_| | |_) | | |_) |  __| | \__ | |_
   | .__/ \__, | .__/|_| .__/ \___|_|_|___/\__|
   | |     __/ | |     | |
   |_|    |___/|_|     |_|
```

## About
This tool performs the same actions as SysInternal's pipelist but performs additional queries to
provide a lot more useful information.

This tool is noisy (see getpipeperms()). It's designed for research not stealth.

This is work in progress... needs a fair bit of TLC.

TODO:
This tool should be able to support mailslots.

Refs:
* http://timgolden.me.uk/pywin32-docs/win32pipe.html
* https://docs.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-getnamedpipeinfo

# Usage
```
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
```

DK @withdk  
https://github.com/withdk  
August 2020  

## Disclaimer
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
