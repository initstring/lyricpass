<meta name="description" content="Password wordlist generator using song lyrics for targeted bruteforce audits / attacks. Useful for penetration testing or security research." />

**Currently tested only with Python 2.7 - need to continue fixing for Python 3+**

# lyricpass
Password wordlist / dictionary generator using song lyrics for targeted bruteforce audits / attacks. Useful for penetration testing or security research.<br>
Easy to use - you give it an artist, you get back a text file with all of their lyrics to use for cracking passwords.


# Overview
People are being encouraged to use longer passwords - specifically multiple words stringed together.
An obvious choice is to use a song lyric from their favorite artist. This seems much more secure than a single word.

The intent of this tool is a POC to prove that this type of password is also insecure, especially if you are able to
find the target's favorite artist (easy enough to do with social media).

This could be used with the password cracker of your choice for testing the security of your own system via brute force methods. It would also be interesting to run to see if it catches any passwords you yourself are currently using.

```
usage: lyricpass.py [-h] [--lower] [--punctuation] artist output

positional arguments:
    artist:         Define a specific artist for song lyric inclusion. Use quotes.
    output:         Output to file name in current directory.

optional arguments:
    -h, --help      show this help message and exit
    --lower         Switches all letters to lower case.
    --punctuation   Preserves the punctuation, which is removed by default
```
Examples:<Br>
```
python lyricpass.py "Rob Zombie" zombie-pass.txt
python lyricpass.py --lower "Stone Temple Pilots" stp.txt
```

# To Do
This is just a very early POC. I still need to work on error checking. I also plan to do the following:
- Provide function to further split lines including a comma (as this could be a logical break)
