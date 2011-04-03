Incessant (j)Stack
==================

Script to call jstack on a jvm instance incessantly, saves threaddumps in a directory, supports options to specifiy interval between threaddumps, number of threaddumps to take and keep.  

Usage
-----
<pre>
Usage: istack.py [options] jvm-process-id
       istack.py -h for options

Options:
  -h, --help            show this help message and exit
  -d DIR, --dir=DIR     Directory to save threaddumps
                        (default: current dir)
  -i INTERVAL, --interval=INTERVAL
                        Interval (seconds) between successive thread dumps
                        (default: 60 seconds)
  -n NUMBER, --number=NUMBER
                        Number of thread dumps to take
                        (default: unlimited)
  -k KEEP, --keep=KEEP  Number of thread dumps to keep
                        (default: 1440)
</pre>

Sample Usages
-------------
1.  Take thread dumps once every minute, indefinitely, keeping latest 1 day worth of dumps (1440).  This is the default without specifying any options
    $ python istack.py <jvm-process-id>

2.  Take thread dumps once every 5 munutes, indefinitely, keeping latest 500 dumps
    $ python istack.py -i 300 -k 500 <jvm-process-id>

3.  Take thread dumps once every 30 seconds for 5 times and save them under dump directory
    $ python istack.py -i 30 -n 5 -d dump <jvm-process-id>


Thread dumps
------------

A directory with YYYYMMDD-hhmm format named with the script invocation time will be created under current directory or under the directory specified with -d option.

Command line of the jvm process which is being jstacked is saved into cmdline.txt file under the above directory

Thread dumps will be saved under the directory with YYYYMMDD-hhmm.txt name formet with jstack invocation time.

For example:
<pre>
    └── 20110402-184224                     # directory with script invocation time
        ├── 20110402-184224.txt             # thread dump 1
        ├── 20110402-184235.txt             # thread dump 2
        ├── 20110402-184246.txt             # .. and so on ..
        ├── 20110402-184256.txt
        ├── 20110402-184307.txt
        ├── 20110402-184318.txt
        ├── 20110402-184329.txt
        ├── 20110402-184339.txt
        ├── 20110402-184350.txt
        └── cmdline.txt                     # jvm process command line
</pre>

Script Exit 
-----------

Script will exit due to one of the following reasons
1.  Input and environment validation failures
2.  Number of thread dumps as specified by -n option were taken successfully
3.  jstack call encountered an error
4.  jstack call did not return within a 60 second timeout

Misc
----
*  Tested with Python 2.6.1 in Mac OSX 10.6.7

Feedback/Issues
---------------
Please use the issue tracker associated with this repository.  Please note that jstack is not available in Windows and Itanium platforms.
