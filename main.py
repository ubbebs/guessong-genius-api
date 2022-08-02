from requests.exceptions import Timeout
import lyricsgenius as genius
import _thread
import os

artistID = 1165795 # set ID of artist 114783 taco/ 40889 que/ 1421023 taconafide/ 1012840 kizo / 31159 bialas / 989939 white2115 / 84456 Żabson / 2232626 young leosia / 1165795 bialaslanek

artistTracks = []

api = genius.Genius('')

artistN = api.artist(artistID) # get dict about artist
artistName = artistN['artist']['name'] # get name from artist's dict
artistCover = artistN['artist']['image_url']
artistBgCover = artistN['artist']['header_image_url']

artistAlbums = api.artist_albums(artistID, per_page=50)
artistAlbumData = artistAlbums['albums']
artistData = {'name':artistName, 'artist_id':artistID, 'cover':artistCover, 'bgcover':artistBgCover}
artistDataStr = str(artistData)
artistFileName = str(artistID)

with open("Artists/" + artistFileName + ".txt", "w", encoding="utf-8") as f: # save file
        f.write(artistDataStr)

print(f"Artist {artistName} ({artistID}) added")

for album in artistAlbumData: # creating files with data about album
    albumID = album['id'] # get ID of an album
    albumName = album['name'] # get name of an album
    albumName = albumName.replace("'", "!@#")
    albumName = albumName.replace('"', "$%^")
    albumCover = album['cover_art_url'] # get cover's src of an album

    albumData = {"name":albumName, "album_id":albumID, "id_artist":artistID, "name_artist":artistName, "cover":albumCover} # set dict for album data
    albumDataStr = str(albumData) # set dict to string
    
    albumFileName = str(albumID) # set albumID to string
    with open("Albums/" + albumFileName + ".txt", "w", encoding="utf-8") as f: # save file
        f.write(albumDataStr)

    print(f"Album {albumName} ({albumID}) added")

for x in range(1,70): # loop to get all of artist's songs
    artistSongData = api.artist_songs(artistID, sort='popularity', per_page=10, page=x) # get dict with song's data
    artistSongName = artistSongData['songs'] # get list as value from dict

    for song in artistSongName: # from list get:
        artistSongID = song['id'] # get song ID
        artistTracks.append(artistSongID) # add songs IDs to list

trackList = artistTracks

print("trackList")

def addingTracks(thname,start,end):
    artistTracks = trackList[start:end]
    for artistTrack in artistTracks: # creating files with data about song

        retries = 0
        while retries < 10:
            try:
                artistTrackData = api.song(artistTrack)
            except Timeout as e:
                retries += 1
                continue

            songID = artistTrackData['song']['id']

            path_tracks = "E:\VS Repos\genius\Tracks"
            tracks_dir_list = os.listdir(path_tracks)
            songFileName = str(songID)
            if ((songFileName + ".txt") in tracks_dir_list):
                break

            songTitle = artistTrackData['song']['title']
            songTitle = songTitle.replace("'", "!@#")
            songTitle = songTitle.replace('"', "$%^")
            songMedia = "None"

            songWriterArtists = artistTrackData['song']['writer_artists']
            
            try:
                songArtist1_id = songWriterArtists[0]['id']
                songArtist1_name = songWriterArtists[0]['name']
            except IndexError:
                songArtist1_id = "None"
                songArtist1_name = "None"
            try:
                songArtist2_id = songWriterArtists[1]['id']
                songArtist2_name = songWriterArtists[1]['name']
            except IndexError:
                songArtist2_id = "None"
                songArtist2_name = "None"
            try:
                songArtist3_id = songWriterArtists[2]['id']
                songArtist3_name = songWriterArtists[2]['name']
            except IndexError:
                songArtist3_id = "None"
                songArtist3_name = "None"
            try:
                songArtist4_id = songWriterArtists[3]['id']
                songArtist4_name = songWriterArtists[3]['name']
            except IndexError:
                songArtist4_id = "None"
                songArtist4_name = "None"

            if artistTrackData['song']['album'] == None:
                songAlbum = "None"
            else:
                songAlbum = artistTrackData['song']['album']['id']

            songCover = artistTrackData['song']['song_art_image_url']
            try:
                songPopularity = artistTrackData['song']['stats']['pageviews']
            except:
                songPopularity = 0

            try:
                for songUrl in artistTrackData['song']['media']:
                    if songUrl['provider'] == 'youtube':
                        songMedia = songUrl['url']
                    else:
                        songMedia = "None"
            except:
                songMedia = "None"

            try:
                songLyrics = api.lyrics(songID)
                if songLyrics:
                    slicePos = songLyrics.find("]") + 2
                    songLyrics = songLyrics[slicePos:]
                    countSlices = songLyrics.count("[")
                    
                    for x in range(countSlices):
                        startPos = songLyrics.find("[")
                        endPos = songLyrics.find("]") + 1
                        substring = songLyrics[startPos:endPos]
                        songLyrics = songLyrics.replace(substring, '')

                    songLyrics = songLyrics.replace("'", "!@#")
                    songLyrics = songLyrics.replace('"', "$%^")
                    songLyrics = songLyrics.replace("\u205f", " ")
                    songLyrics = songLyrics.replace("\u2005", " ")
                    songLyrics = songLyrics.replace("\xa0", " ")
                    songLyrics = songLyrics.replace("\xad", " ")
                    sliceWord = "Embed"
                    try:
                        sliceWordPos = songLyrics.find(sliceWord)
                        sliceString = songLyrics[sliceWordPos:]
                        songLyrics = songLyrics.replace(sliceString, '')

                        repeat = True

                        while repeat:
                            sliceWordPos -= 1

                            try:
                                int(songLyrics[sliceWordPos])
                                sliceString = songLyrics[sliceWordPos:]
                                songLyrics = songLyrics.replace(sliceString, '')
                            except ValueError:
                                break
                    except IndexError:
                        songLyrics = songLyrics

            except Timeout as e:
                retries += 1
                continue

            if songLyrics == None:
                songLyrics = "None"

            songData = {"title":songTitle, "track_id":songID, "id_artist1": songArtist1_id, "name_artist1": songArtist1_name, "id_artist2": songArtist2_id, "name_artist2": songArtist2_name, "id_artist3": songArtist3_id, "name_artist3": songArtist3_name, "id_artist4": songArtist4_id, "name_artist4": songArtist4_name, "id_album": songAlbum, "cover":songCover, "popularity":songPopularity, "yt_url":songMedia, "lyrics":songLyrics}
            songDataStr = str(songData)
            
            with open("Tracks/" + songFileName + ".txt", "w", encoding="utf-8") as f:
                f.write(songDataStr)
            
            print(f"{thname} / Dodano utwór / Title: {songTitle}, ID: {songID}, Popularity: {songPopularity}")
            break
    print(f"{thname} ENDED")

trackListLen = len(trackList)
print(f"Liczba utworów: {trackListLen}")
modulo = trackListLen % 12
lenP = (trackListLen + 12 - modulo) / 12
lenP = int(lenP)

try:
    _thread.start_new_thread( addingTracks, ("T1", 0, lenP, ) )
    _thread.start_new_thread( addingTracks, ("T2", lenP, lenP*2, ) )
    _thread.start_new_thread( addingTracks, ("T3", lenP*2, lenP*3, ) )
    _thread.start_new_thread( addingTracks, ("T4", lenP*3, lenP*4, ) )
    _thread.start_new_thread( addingTracks, ("T5", lenP*4, lenP*5, ) )
    _thread.start_new_thread( addingTracks, ("T6", lenP*5, lenP*6, ) )
    _thread.start_new_thread( addingTracks, ("T7", lenP*6, lenP*7, ) )
    _thread.start_new_thread( addingTracks, ("T7", lenP*7, lenP*8, ) )
    _thread.start_new_thread( addingTracks, ("T7", lenP*8, lenP*9, ) )
    _thread.start_new_thread( addingTracks, ("T7", lenP*9, lenP*10, ) )
    _thread.start_new_thread( addingTracks, ("T7", lenP*10, lenP*11, ) )
    _thread.start_new_thread( addingTracks, ("T7", lenP*11, lenP*12, ) )
except:
    print("Error: unable to start thread")

while 1:
    pass