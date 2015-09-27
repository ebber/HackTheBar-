import sys
#import MOD

def tb_lineno(tb):
    c = tb.tb_frame.f_code
    if not hasattr(tb.tb_frame.f_code, 'co_lnotab'):
        return tb.tb_lineno
    line = tb.tb_frame.f_code.co_firstlineno
    addr = 0
    for i in range(0, len(tb.tb_frame.f_code.co_lnotab), 2):
        addr = addr + ord(tb.tb_frame.f_code.co_lnotab[i])
        if addr > tb.tb_lasti:
            break
        line = line + ord(tb.tb_frame.f_code.co_lnotab[i+1])
    return line

try:
    #Check if remote download needs to be activate, by checking if the file run_script is exist
    value = 1
    try:
        l_fileErr=open('/sys/run_script.txt','rb')
        l_fileErr.close()
    except IOError, details:
        value = 0
    if value:
        import main_load
    else:
        import Weiss
        l_Weiss=Weiss.Weiss()
        l_Weiss.main()
except:
    type, value, tb = sys.exc_info()
    print ('============= An Exception occurs ============\r\n')
    print ('Error Type: %s\r\nError Value: %s\r\n' % (type,value))
    l_fileErr = open('Errors.txt','wb')
    l_fileErr.write('============= An Exception occurs ============\r\n')
    l_fileErr.write('Error Type: %s\r\nError Value: %s\r\n' % (type,value))
    while tb is not None:
        print ('\tFile "%s", line %d, in %s\r\n' % (tb.tb_frame.f_code.co_filename, tb_lineno(tb),tb.tb_frame.f_code.co_name))
        l_fileErr.write('\tFile "%s", line %d, in %s\r\n' % (tb.tb_frame.f_code.co_filename, tb_lineno(tb),tb.tb_frame.f_code.co_name))
        tb = tb.tb_next
    l_fileErr.close()
    #MOD.watchdogEnable(1)  #enable the watchdog
    #while 1:
    #  pass
