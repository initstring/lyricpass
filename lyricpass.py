import argparse
from bs4 import BeautifulSoup
import requests
import sys


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
parser.add_argument("--lower", help="Switches all letters to lower case.", action='store_true')
args = parser.parse_args()

artist = args.artist
outfile = args.output


# The web site uses underscores in place of spaces. This function will format for us:
def create_artist_url(a):
    a = a.replace(' ', '_')
    url = 'http://lyrics.wikia.com/wiki/' + a
    return url

# The site has a standard format for URLs. After we find the song names, we can use this to get the URL:
def create_song_url(song, artist):
    song = song.replace(' ', '_')
    artist = artist.replace(' ', '_')
    url = 'http://lyrics.wikia.com/wiki/' + artist + ':' + song
    return url


# This function attempts to create a list of links to songs based on the artist put in on the command line.
# Later, we will use these song names to go looking for the lyrics:
def get_songs(artisturl, artist):
    cleanlinks = []
    response = requests.get(artisturl)                       # We want to scrape the artist's landing page
    soup = BeautifulSoup(response.content, "html.parser")
    rawlinks = soup.select("ol li b a")                      # On that page, find the bulleted song lists
    for l in rawlinks:
        url = create_song_url(l.text, artist)                # Create a new link based on artist and song name
        cleanlinks.append(url)                               # Stash this song link in a list to return
    return cleanlinks


# After we know the song names, we can use the artist name and the url function above to go find the actual lyrics.
# This function does some basic cleaning of HTML tags out of the return strings. I found that unexpected data
# is occasionally returned and generated errors trying to append to a list, so we will work around that with try
# and except:
def get_lyrics(songurl):
    l = []
    response = requests.get(songurl)                            # Now we scrape each individual song page
    soup = BeautifulSoup(response.content, "html.parser")
    lyricbox = soup.find('div', {'class': 'lyricbox'})          # The lyrics are stored in a div tag called lyricbox
    if lyricbox:
        for line in lyricbox:                                   # Grab the good text out of the lyricbox
            if line and '<' not in str(line) and '\' not in str(line)':
                try:
                    l.append(str(line))
                except:
                    continue
    print ("Found " + str(len(l)) + " lines of lyrics")
    return l


# This function only has an effect when optional parameters are specified, such as output in lowercase:
def format_lyrics(rawlyrics):
    if args.lower:
        formatted = [element.lower() for element in rawlyrics]
    else:
        formatted = rawlyrics
    return formatted


# This function will append the found lyrics to a file in the current directory:
def write_file(l, o):
    file = open(o, 'a')
    for line in l:
        try:
            file.write(str(line) + '\n')
        except:
            continue


def main():
    lyrics = []
    print('Looking for lyrics from ' + artist + ' and writing to file: ' + outfile)

    artisturl = create_artist_url(artist)               # create a workable URL
    songlinks = get_songs(artisturl, artist)            # find all the songs for this artist
    for s in songlinks:
        print("Getting lyrics for " + s)
        for l in get_lyrics(s):                         # get a list of lyric lines
            try:
                lyrics.append(l)                        # append found lines to master list
            except:
                continue
    lyrics = format_lyrics(lyrics)                      # format lyrics as specified in arguments
    print("*********************")
    print("Now writing output file...")
    write_file(lyrics, outfile)                         # write the output file




if __name__ == '__main__':
    main()