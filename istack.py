#!/usr/bin/env python
# -------------------------------------------------------------------------------
#  Incessant (j)Stack
#  ------------------
# Script which calls _jstack_ on a jvm instance incessantly, saves thread dumps 
# in a directory, supports options to specifiy interval between taking thread 
# dumps, number of thread dumps to take and keep.
# 
#  Senthil Vaiyapuri - April 2011
# -------------------------------------------------------------------------------
from optparse import OptionParser
from subprocess import call, Popen, PIPE
import time
import sys
import os
import signal
import glob

__version__ = "0.1"

# setup command line options
usage = "usage: %prog [options] jvm-process-id\n       %prog -h for options"
parser = OptionParser(usage=usage)
parser.add_option("-d", "--dir", dest="dir", default=".",
                  help="Directory to save threaddumps \
                        (default: current dir)")
parser.add_option("-i", "--interval", dest="interval", type="int", default=60,
                  help="Interval (seconds) between successive thread dumps \
                        (default: 60 seconds)")
parser.add_option("-n", "--number", dest="number", type="int", default=sys.maxint,
                  help="Number of thread dumps to take \
                        (default: unlimited)")
parser.add_option("-k", "--keep", dest="keep", type="int", default=1440,
                  help="Number of thread dumps to keep \
                        (default: 1440)")

def shell(args):
    try:
        p = call(args, stdout=PIPE, stderr=PIPE)
        return p == 0
    except OSError, e:
        return False

def validate(options, args):
    if len(args) != 1:
        parser.print_usage()
        print  "Error: Please specify jvm-process-id"
        exit(1)

    # check whether jvm process exists
    jvm_pid = args[0]
    if not shell(["ps", "-p", jvm_pid]):
        print "Error: jvm process (%s) does not exist" % jvm_pid
        exit(1)
    
    # check whether jstack exists in path
    if not shell(["which", "jstack"]):
        print "Error: jstack executable is not in PATH"
        exit(1)

    return jvm_pid

def setup(out_dir):
    try:
        os.makedirs(out_dir)
    except OSError, e:
        print "Error: creating directory in %s failed" % options.dir
        print "      ",e
        exit(1)

def get_output(args):
    p = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    return (p.returncode, out, err)

def alarm_handler(signum, frame):
    print "Error: alarm raised, jstack command timed out (60 seconds), exiting"
    exit(1)

def manage_dumps(options, out_dir):
    dumps = glob.glob(out_dir+"/[0-9]*.txt")
    delete = len(dumps) - options.keep
    while delete > 0:
        try:
            os.remove(dumps[delete-1])
        except:
            pass
        finally:
            delete -= 1

def run(options, jvm_pid, out_dir):
    # save jvm process command line
    try:
        retcode, out, err = get_output(["ps","-o","command","-p", jvm_pid])
    except:
        pass
    else:
        if retcode == 0:
            with open(out_dir+"/cmdline.txt","w") as c:
                c.write(out)

    signal.signal(signal.SIGALRM, alarm_handler)

    # atlast, incessant jstack
    count = options.number
    while count > 0:
        fname = out_dir + "/" + get_time() + ".txt"
        try:
            signal.alarm(60)
            retcode, out, err = get_output(["jstack", jvm_pid])
            signal.alarm(0)
        except:
            print "Error: jstack command failed with exception. exiting"
            exit(1)
        else:
            if retcode != 0:
                print "Error: jstack command failed. exiting"
                print "  retcode : ",retcode
                print "  stdout  : ",out
                print "  stderr  : ",err
                exit(1)

            # write out the thread dump
            with open(fname, "w") as f:
                f.write(out)

            manage_dumps(options, out_dir)
            count -= 1
            if count > 0:
                time.sleep(options.interval)

def get_time():
    return time.strftime('%Y%m%d-%H%M%S')

if __name__ == '__main__':
    # mark time
    run_time = get_time()

    # parae arguments and validate
    (options, args) = parser.parse_args()
    jvm_pid = validate(options, args)

    # setup output directory
    out_dir = options.dir + "/" + run_time
    setup(out_dir)

    # run
    run(options, jvm_pid, out_dir)
