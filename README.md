Incessant (j)Stack
==================

Script which calls _jstack_ on a jvm instance incessantly, saves thread dumps in a directory, supports options to specifiy interval between taking thread dumps, number of thread dumps to take and keep.  

### Usage
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

### Sample Usages
* Take thread dumps once every minute, indefinitely, keeping latest 1 day worth of dumps (1440).  This is the default without specifying any options.
<pre>
    $ python istack.py &lt;jvm-process-id&gt;
</pre>

* Take thread dumps once every 5 munutes, indefinitely, keeping latest 500 dumps
<pre>
    $ python istack.py -i 300 -k 500 &lt;jvm-process-id&gt;
</pre>

* Take thread dumps once every 30 seconds for 5 times and save them under dump directory
<pre>
    $ python istack.py -i 30 -n 5 -d dump &lt;jvm-process-id&gt;
</pre>

### Dependency
* _jstack_ in PATH

### Thread dumps
A directory with _YYYYMMDD-hhmmss_ format named with the script invocation time will be created under current directory or under the directory specified with -d option.

Command line of the jvm process which is being jstacked is saved into _cmdline.txt_ file under the above directory

Thread dumps will be saved under the directory with _YYYYMMDD-hhmmss.txt_ name formet with _jstack_ invocation time.

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

### Script Exit 
Script will exit due to one of the following reasons

1. Input and environment validation failures
2. Number of thread dumps as specified by -n option were taken successfully
3. _jstack_ call encountered an error
4. _jstack_ call did not return within a 60 second timeout

### Testing
* Tested with Python 2.6.1, jstack (bundled with JDK 1.6.0_24) in Mac OSX 10.6.7

### Feedback/Issues
Please use the issue tracker associated with this repository.  Please note that _jstack_ is not available in Windows and Itanium platforms.

### References
* [jstack](http://download.oracle.com/javase/1.5.0/docs/tooldocs/share/jstack.html)
