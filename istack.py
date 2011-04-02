#!/usr/bin/env python
# -------------------------------------------------------------------------------
#  Incessant (j)Stack
#  ------------------
#  Script to call jstack on a jvm instance incessantly, saves threaddumps in a 
#  directory, supports options to specifiy interval between threaddumps, number
#  of threaddumps to take and keep.
# 
#  Senthil Vaiyapuri - April 2011
# -------------------------------------------------------------------------------
from optparse import OptionParser
import time
from subprocess import call, Popen, PIPE

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
parser.add_option("-n", "--number", dest="number", type="int", default=-1,
                  help="Number of thread dumps to take \
                        (default: unlimited)")
parser.add_option("-k", "--keep", dest="number", type="int", default=1440,
                  help="Number of thread dumps to keep \
                        (default: 1440)")


# alarm handler

# purge old file

# jstack

# setup dirs

def shell(cmdline):
    try:
        p = call("%s" % cmdline, shell=True, stdout=PIPE, stderr=PIPE)
        return p == 0
    except OSError, e:
        return False

def validate(options, args):
    if len(args) != 1:
        parser.print_usage()
        print  "Error: Please specify jvm-process-id"
        exit(1)

    # check whether jvm process exists
    jvm_pid = int(args[0])
    if not shell("ps -p %d" % jvm_pid):
        print "Error: jvm process (%d) does not exist" % jvm_pid
        exit(1)
    
    # check whether jstack exists in path
    if not shell("which jstack"):
        print "Error: jstack executable is not in PATH"
        exit(1)

    return jvm_pid

def setup(options, jvm_pid, run_time):
    pass

def run(options, jvm_pid, run_time):
    pass

# get time 
def get_time():
    return time.strftime('%Y%m%d-%H%M')

if __name__ == '__main__':
    # mark time
    run_time = get_time()

    # parae arguments and validate
    (options, args) = parser.parse_args()
    jvm_pid = validate(options, args)

    # setup output directory
    setup(options, jvm_pid, run_time)

    # run
    run(options, jvm_pid, run_time)
