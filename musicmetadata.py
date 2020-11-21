import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='87ad7f581a9543029f672950ff6c61c3',
                 client_secret='d79ef4301cdd4aae84b5e813d95aa994'))

#take input from user
user_ip=str(input('enter the name of the song\n'))

track1 = sp.search(q=' track:' + user_ip, type='track',limit=10)
track_id = sp.search(q=' track:' + user_ip, type='track')
'''
#print the uri of the song
print(track_id['tracks']['items'][0]['uri'])
print('\n')
'''
#print the name of artist
print('artists found: \n')
for i in range(0,10):
        print(track_id['tracks']['items'][i]['album']['artists'][0]['name'])
print('\n')
index=int(input('which artist are you looking for?(1-10)'))
index=index-1
print('\n')

#print the official name of the song
print('Official song name: ' + track1['tracks']['items'][index]['name'])
print('\n')

#print the length of the song
sec=float(track1['tracks']['items'][index]['duration_ms'])
sec=sec/1000
sec = sec % (24 * 3600) 
hour = sec // 3600
sec %= 3600
minutes = sec // 60
sec %= 60
print("Track length: %02d:%02d minutes\n" % (minutes, sec)) 

#print the name of the album
print('Album: ' + track1['tracks']['items'][index]['album']['name'])

#print the genre of the artist
result = sp.search(q='track:' + user_ip,type = 'track')
track = result['tracks']['items'][index]
artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
print("artist genres:", artist["genres"])

#print genre of album
album = sp.album(track["album"]["external_urls"]["spotify"])
print("album genres:", album["genres"])

#print release date of album
print("album release-date:", album["release_date"])

#print the popularity of the track
print('Popularity(0-100): ' + str(track1['tracks']['items'][index]['popularity']))
