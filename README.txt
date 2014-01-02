sebadel - 2014/01/02

Disclaimer
---------
Use this at your own risk.
Running this script will alter some files.
Do not execute it unless you understand what it's doing.

Purpose
-------
Parses a website's directory, looking up for suspiciously long lines in files with .php extension.
If it finds a suspicious first line, it will clean it up, saving a copy under a quarantine folder.

Context
-------
One of our webservers has been targeted by some PHP malware.
The malware was adding some PHP encoded string on the first line of most .php files.
I ended up writing this quick script to automate the process of cleaning the files.
