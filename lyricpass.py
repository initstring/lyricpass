#!/usr/bin/env python3
"""
Utility to scrape lyrics from https://lyrics.com

Usage:
lyricspass.py -a <artist>
lyricpass.py -i <file with multiple artists>

Example:
python lyricpass.py -a "Rob Zombie"
python lyricpass.py -i /tmp/artists.txt

Outputs two files:
raw-lyrics.txt <everything>
wordlist.txt <cleaned passphrases>

Tool by initstring. If you're into cracking complex passwords, check out
github.com/initstring/passphrase-wordlist for more fun!
"""

import argparse
import requests
import datetime
import os
import sys
import re

SITE = "https://www.lyrics.com/"
LYRIC_FILE = "raw-lyrics-{:%Y-%m-%d-%H.%M.%S}".format(datetime.datetime.now())
PASS_FILE = "wordlist-{:%Y-%m-%d-%H.%M.%S}".format(datetime.datetime.now())


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

    parser.add_argument("--min", type=int, default=8,
                        help="Minimum passphrase length. Default=8")
    parser.add_argument("--max", type=int, default=40,
                        help="Minimum passphrase length. Default=40")

    args = parser.parse_args()

    if args.infile:
        if not os.access(args.infile, os.R_OK):
            print("[!] Cannot access input file, exiting")
            sys.exit()

    return args

def make_phrases(line, args):
    """
    Cleans raw lyrics into usable passphrases
    """
    clean_lines = []
    final_lines = []

    # Allow only letters, numbers, spaces, and some punctuation
    allowed_chars = re.compile("[^a-zA-Z0-9 '&]")

    # Lowercase everything and deal with common punctuation
    line = line.lower()
    line = re.sub(r'[-_]', ' ', line)

    # The following lines attempt to remove accented characters, as the
    # tool is focused on Engligh-language passwords.
    line = re.sub('[àáâãäå]', 'a', line)
    line = re.sub('[èéêë]', 'e', line)
    line = re.sub('[ìíîï]', 'i', line)
    line = re.sub('[òóôõö]', 'o', line)
    line = re.sub('[ùúûü]', 'u', line)
    line = re.sub('[ñ]', 'n', line)

    # Gets rid of any remaining special characters in the name
    line = allowed_chars.sub('', line)

    # Shrinks down multiple spaces
    line = re.sub(r'\s\s+', ' ', line)

    # If line has an apostrophe make a duplicate without
    if "'" in line:
        clean_lines.append(re.sub("'", "", line))

    # Making duplicating phrases including and / &
    if ' and ' in line:
        clean_lines.append(re.sub(' and ', ' & ', line))
    if '&' in line:
        newline = re.sub('&', ' and ', line)
        newline = re.sub(r'\s+', ' ', newline).strip()
        clean_lines.append(newline)

    # Add what is left to the list
    clean_lines.append(line)

    # Only keep items in the acceptable length
    for item in clean_lines:
        if args.max >= len(item) >= args.min:
            final_lines.append(item)

    return final_lines

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

    response = requests.get(query_url)
    html = response.text

    # The songs are stored by a unique ID
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

    # The "print" URL shows us the easiest to decode version of the song
    url_list = [SITE + "db-print.php?id=" + id for id in song_ids]

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

        response = requests.get(url)
        html = response.text

        lyrics = re.findall(regex, html)

        # We should always have a match... but if not, skip this url
        if not lyrics:
            print("\n[!] Found no lyrics at {}".format(url))
            continue

        lyrics = re.split(newline, lyrics[0])

        write_data(LYRIC_FILE, lyrics)

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
    final_phrases = set()

    # First, we grab all the lyrics for a given artist.
    # The scrape_lyrics function will write the raw lyrics to an output
    # file as it goes, which may come in handy if the program exits early
    # due to an error.
    for artist in artists:
        print("[+] Looking up artist {}".format(artist))
        url_list = build_urls(artist)
        if not url_list:
            continue
        raw_words.update(scrape_lyrics(url_list))

    # Now we will apply some rules to clean all the raw lyrics into a base
    # passphrase file that can be used for cracking.
    for lyric in raw_words:
        phrases = make_phrases(lyric, args)
        final_phrases.update(phrases)

    # Write out the cleaned passphrases to a file
    write_data(PASS_FILE, final_phrases)

    print("[+] All done!")
    print("")
    print("Raw lyrics: {}".format(LYRIC_FILE))
    print("Passphrases: {}".format(PASS_FILE))


if __name__ == '__main__':
    main()
