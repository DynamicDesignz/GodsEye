import ftplib as fl
import time

def refr():
        
    f = fl.FTP('-host-', '-user-', '-password-')
    f.cwd('metadata')
    files = f.nlst('*.*')

    for i in files:
        fileh = open(i, 'wb')
        f.retrbinary('RETR '+i, fileh.write)

    f.quit()
        
if __name__ == '__main__':
    while True:
        print 'refreshing...'
        refr()
        time.sleep(60)
        
        
