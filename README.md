# lyricpass
Generates password lists with song lyrics based on a given artist

usage: lyricpass.py [-h] [--lower] artist output

positional arguments: <Br>
&nbsp;&nbsp;&nbsp;&nbsp;artist:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Define a specific artist for song lyric inclusion. Use quotes.<br>
&nbsp;&nbsp;&nbsp;&nbsp;output&nbsp;&nbsp;&nbsp;&nbsp;Output to file name in current directory.

optional arguments:
&nbsp;&nbsp;&nbsp;&nbsp;-h,&nbsp;&nbsp;&nbsp;&nbsp;--help  show this help message and exit
&nbsp;&nbsp;&nbsp;&nbsp;--lower&nbsp;&nbsp;&nbsp;&nbsp;Switches all letters to lower case.

Examples:
python lyricpass.py "Rob Zombie" zombie-pass.txt
python lyricpass.py --lower "Stone Temple Pilots" stp.txt

# Overview
People are being encouraged to user longer passwords - specifically multiple words stringed together.
An obvious choice is to use a song lyric from their favorite artist. This seems much more secure than a single word.

The intent of this tool is a POC to prove that this type of password is also insecure, especially if you are able to
find the target's favorite artist (easy enough to do with social media).

# To Do
This is just a very early POC. I still need to work on error checking. I also plan to do the following:
- Provide options for punctuation removal
- Provide function to further split lines including a comma (as this could be a logical break)