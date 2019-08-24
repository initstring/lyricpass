#!/usr/bin/env python3
"""
Utility to scrape lyrics from https://lyrics.wikia.com

Used as a tool to generate raw input for the cleanup.py script in the password
cracking project at github.com/initstring/passphrase-wordlist

Usage:
lyricspass.py -a <artist>
lyricpass.py -i <file with multiple artists>

Example:
python lyricpass.py -a "Rob Zombie"
python lyricpass.py -i /tmp/artists.txt

Outputs two files:
raw-lyrics.txt <everything>
passphrases.txt <cleaned passphrases>
"""

import argparse
import urllib.request
import os
import sys
import re

SITE = "https://www.lyrics.com/"


def parse_args():
    """
    Handle user-passed parameters
    """
    desc = "Scrape song lyrics from wikia.com"
    parser = argparse.ArgumentParser(description=desc)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-a", "--artist", type=str, action="store",
                       help="Single artist to scrape")
    group.add_argument("-i", "--infile", type=str, action="store",
                       help="File containing one artist per line to scrape")

    args = parser.parse_args()

    if args.infile:
        if not os.access(args.infile, os.R_OK):
            print("[!] Cannot access input file, exiting")
            sys.exit()

    return args

def parse_artists(args):
    """
    Return a list of song artists for parsing
    """
    whitelist = re.compile('[^a-zA-Z0-9-+]')
    artists = []

    if args.artist:
        raw_artists = [args.artist,]
    else:
        with open(args.infile, encoding="utf-8", errors="ignore") as infile:
            raw_artists = infile.readlines()

    for artist in raw_artists:
        artist = artist.replace(" ", "+")
        artist = whitelist.sub("", artist)
        if artist not in artists:
            artists.append(artist)

    return artists

def build_urls(artist):
    """
    Creates a list of song URLs for a specific artist
    """
    not_found = "We couldn't find any artists matching your query"
    query_url = SITE + "/artist.php?name=" + artist
    song_ids = []
    regex = re.compile(r'href="/lyric/(.*?)/')

    with urllib.request.urlopen(query_url) as response:
        html = response.read().decode()

    song_ids = re.findall(regex, html)

    if not_found in html:
        print("[!] Artist {} not found, skipping".format(artist))

        # Clear out the "suggested" songs it finds in this scenario
        song_ids = []
    elif not song_ids:
        print("[!] No songs found for {}, skipping".format(artist))
    else:
        print("[+] Found {} songs for artists {}"
              .format(len(song_ids), artist))

    url_list = [SITE + "print.php?id=" + id for id in song_ids]
    return url_list

def write_data(outfile, data):
    """
    Generic helper function to write text to a file
    """
    with open(outfile, "a") as open_file:
        for line in data:
            if line:
                open_file.write(line + '\n')

def scrape_lyrics(url_list):
    """
    Scrapes raw lyric data from a list of URLs
    """
    regex = re.compile(r"<pre.*?>(.*?)</pre>", re.DOTALL)
    newline = re.compile(r"\r\n|\n")

    deduped_lyrics = set()

    current = 1
    total = len(url_list)

    for url in url_list:
        print("Checking song {}/{}...       \r".format(current, total), end="")

        with urllib.request.urlopen(url) as response:
            html = response.read().decode()

        lyrics = re.findall(regex, html)[0]
        lyrics = re.split(newline, lyrics)

        write_data('raw-lyrics.txt', lyrics)

        deduped_lyrics.update(lyrics)

        current += 1

    return deduped_lyrics


def main():
    """
    Main program function
    """
    args = parse_args()
    artists = parse_artists(args)

    raw_words = set()

    for artist in artists:
        print("[+] Looking up artist {}".format(artist))
        url_list = build_urls(artist)
        if not url_list:
            continue
        raw_words.update(scrape_lyrics(url_list))

    # TO DO: Implement cleaning function before writing this one.
    write_data("wordlist.txt", raw_words)

    print("[+] All done! Check out raw-lyrics.txt and wordlist.txt in your"
          " current directory.")




if __name__ == '__main__':
    main()
