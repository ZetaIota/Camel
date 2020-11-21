from imdb import IMDb

# create an instance of the IMDb class
ia = IMDb()

#get movie name as input
name=input('enter the name of the movie or tv show\n')

#searching keyword
search = ia.search_movie(name)

#find movie ID
id= search[0].movieID

#getting official movie name
movie_name=ia.get_movie(id)
print('official name of movie or tv show is: ' + str(movie_name))

#print the genres of the movie
print('Genres:')
genre=movie_name['genres']
print(genre)

#print the length ofhe movie
length= movie_name['runtimes']
print('length of the movie or one episode in minutes: ' + str(length[0]))

#print number of seasons of tv show
try:
    print('Number of seasons:' + str(movie_name.data['number of seasons']))
except:
    print('\n')

#print rating of the movie
rating= movie_name.data['rating']
print('rating :' + str(rating))

#print year released
year= movie_name.data['year']
print('year released :' + str(year))

#print the movie language
lang= movie_name.data['language codes']
print('languages :' + str(lang))
