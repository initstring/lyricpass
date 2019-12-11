# lyricpass
Generate lyric-based passphrase wordlists for offline password cracking.

Provide a single artist or a file containing one artists per line. The tool will generate two files for you:
- raw-lyrics.txt (all lyrics from all songs)
- wordlist.txt (likely passphrase candidates)

You can use `wordlist.txt` with something like hashcat and a good set of rules. I recommend combining it with my passphrase cracking project [available here](https://github.com/initstring/passphrase-wordlist). 

## Utilization

```
usage: lyricpass.py [-h] (-a ARTIST | -i INFILE)

optional arguments:
  -h, --help            show this help message and exit
  -a ARTIST, --artist ARTIST
                        Single artist to scrape
  -i INFILE, --infile INFILE
                        File containing one artist per line to scrape
  --min MIN             Minimum passphrase length. Default=8
  --max MAX             Minimum passphrase length. Default=40

```

Examples:

```
lyricpass.py -a "Rob Zombie"
lyricpass.py -i /tmp/my-fav-artists.txt
```
