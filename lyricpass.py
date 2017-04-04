import argparse
from PyLyrics import *
from bs4 import BeautifulSoup
import requests


# Creating a class for the parser to gracefully handle errors:
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


# Handle the arguments before executing the main functions:
parser = MyParser()
parser.add_argument("artist", type=str, help="Define a specific artist for song lyric inclusion. Please  place \
                                               the artist name in quotes.", action="store")
parser.add_argument("output", type=str, help="Output to file name in current directory.", action="store")
args = parser.parse_args()

artist = args.artist
outfile = args.output


def create_artist_url(a):
    a = a.replace(' ', '_')
    url = 'http://lyrics.wikia.com/wiki/' + a
    return url

def create_song_url(song, artist):
    song = song.replace(' ', '_')
    artist = artist.replace(' ', '_')
    url = 'http://lyrics.wikia.com/wiki/' + artist + ':' + song
    return url


def get_songs(artisturl, artist):
    cleanlinks = []
    response = requests.get(artisturl)
    soup = BeautifulSoup(response.content, "html.parser")
    rawlinks = soup.select("ol li b a")
    for l in rawlinks:
        url = create_song_url(l.text, artist)
        cleanlinks.append(url)
    return cleanlinks


def get_lyrics(songurl):
    l = []
    response = requests.get(songurl)
    soup = BeautifulSoup(response.content, "html.parser")
    lyricbox = soup.find('div', {'class': 'lyricbox'})
    try:
        for line in lyricbox:
            if line and '<' not in str(line) and '\' not in str(line)':
                l.append(str(line))
    except:
        return
    return l


def format_lyrics(rawlyrics):
    cleanlyrics = rawlyrics
    return cleanlyrics


def write_file(l, o):
    file = open(o, 'a')
    try:
        for line in l:
            file.write(str(line) + '\n')
    except:
        return


def main():
    lyrics = []
    print('Looking for lyrics from ' + artist + ' and writing to file: ' + outfile)
    artisturl = create_artist_url(artist)
    songlinks = get_songs(artisturl, artist)
    for s in songlinks:
        print("Getting lyrics for " + s)
        lyrics.append(get_lyrics(s))
    lyrics = format_lyrics(lyrics)
    print("*********************")
    print("Now writing output file...")
    for song in lyrics:
        write_file(song, outfile)




if __name__ == '__main__':
    main()