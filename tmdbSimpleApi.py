from PIL import Image
from requests.models import HTTPError
# This is the one I'm going to use, launch from anaconda navigator for the right virtual enviroment
import tmdbsimple as tmdb
import requests
from tmdbsimple import search
import tmdbsimple
from tmdbsimple.tv import TV

tmdb.API_KEY = 'a2b67da805cffb9ba951a0f56da1e603'
tmdb.REQUESTS_SESSION = requests.session()

# Title is movie = tmdb.Movies(code) movie.info()['title']

def getId(show):
    try:
        search = tmdb.Search()
        showId = search.tv(query=show)['results'][0]['id']
        return showId
    except HTTPError as e:
        # Maybe deal with this better
        # ALT-OUTPUT empty list
        return None
    except IndexError as e:
        return None

def getIdPerson(person):
    try:
        search = tmdb.Search()
        personId = search.person(query=person)['results'][0]['id']
        return personId
    except HTTPError as e:
        # Maybe deal with this better
        # ALT-OUTPUT empty list
        return None


def getRecommendations(show, n):
    # n = number of reccomendations
    # Returns top 8 (if possible) reccomendations of the show inputted
    # List of dictionaries containing 'title', 'tagline' and 'poster_path'
    try:
        recs = []
        showId = getId(show)
        #showId = show

        reccomendations = tmdb.TV.recommendations(tmdb.TV(showId))
        reccomendedShows = reccomendations['results']
        noReccomedations = reccomendations['total_results']

        for i in range(min(n, noReccomedations)):
            curId = int(reccomendedShows[i]['id'])
            curInfo = tmdb.TV(int(curId)).info()
            recs.append(
                {'title': curInfo['name'], 'tagline': curInfo['tagline'], 'poster_path': curInfo['poster_path']})

    # OUTPUT List (length 0 - 5) with keys:
    # {'title', 'tagline', 'poster_path'}
        return recs

    except HTTPError as e:
        # Maybe deal with this better
        # ALT-OUTPUT empty list
        return None


def getShow(show):
    # Returns dict of title, overview, created by, genres, seasons, tagline, poster path for show inputted
    try:
        search = tmdb.Search()
        response = search.tv(query=show)
        noResults = response['total_results']
        if noResults == 1:
            showId = response['results'][0]['id']
            showResults = tmdb.TV(int(showId)).info()
            resultsList = [{'title': showResults['name'], 'overview': showResults['overview'], 'creator': showResults['created_by'],
                'genres': showResults['genres'], 'seasons': showResults['seasons'], 'tagline': showResults['tagline'], 'poster_path': showResults['poster_path']}]
        elif noResults > 1:
            resultsList = []
            for i in range(noResults):
                showId = response['results'][i]['id']
                showResults = tmdb.TV(int(showId)).info()
                resultsList.append({'title': showResults['name'], 'overview': showResults['overview'], 'creator': showResults['created_by'],
                                   'genres': showResults['genres'], 'seasons': showResults['seasons'], 'tagline': showResults['tagline'], 'poster_path': showResults['poster_path']})
        # OUTPUT List (undetermined length, probobably 20+ entries) of dictionaries with keys:
        # {'title', 'overview', 'creator', 'genres'(list), 'seasons'(dict), 'tagline', 'poster_path'}
        return resultsList

    except HTTPError as e:
        # ALT-OUTPUT empty list
        return None


def getCast(show):
    # Returns a list of actors from a show
    castList = []
    try:
        showId = getId(show)
        cast = tmdb.TV(showId).credits()['cast']

        for i in range(10):
            # Is there a gender neutral term for actor?
            curCast = cast[i]
            curId = curCast['id']
            # This curProfile thing could easily break if they don't have a profile
            if len(tmdb.People(curId).images()['profiles']) > 0:
                curProfile = tmdb.People(curId).images()['profiles'][0]
            else:
                curProfile = None

            castList.append(
                {'name': curCast['name'], 'character': curCast['character'], 'profile': curProfile})
        # OUTPUT list of dicts with keys:
        # {'name', 'character', 'profile'(dict if present, none if not present)}
        return castList 

    except HTTPError as e:
            # ALT-OUTPUT empty list
            return None

def getCastMemberPage(member):

    castMember = tmdb.People(member)
    
    info = castMember.info()
    credits = castMember.tv_credits()['cast']
    creditsList = []
    for i in range(3):
        creditsList.append({'name' : credits[i]['original_name'], 'description' : credits[i]['overview'], 'image' : credits[i]['poster_path']})
    return ({'name' : info['name'], 'birthday' : info['birthday'], 'credits' : creditsList, 'image' : castMember.images()['profiles'][0]['file_path']})

def getPopular(n):
    if n == 1:
        popular = requests.get('https://api.themoviedb.org/3/discover/tv?api_key={}&sort_by=popularity.desc'.format(tmdb.API_KEY)).json()['results'][0]
        return popular
    else:
        popularList = []
        for i in range(n):
            popularList.append(requests.get('https://api.themoviedb.org/3/discover/tv?api_key={}&sort_by=popularity.desc'.format(tmdb.API_KEY)).json()['results'][i])
        return popularList

def getShowPage(showName):
    try:
        showId = getId(showName)
        show = tmdb.TV(showId)
        showInfo = show.info()
        showImages = show.images()
        castList = []
        showCast = show.credits()['cast']


        for i in range(3):
            curCast = showCast[i]
            castList.append({'name' : curCast['name'], 'character' : curCast['character'], 'image' : curCast['profile_path']})


        return {'title' : showInfo['name'], 'description' : showInfo['overview'], 'poster_path' : showImages['posters'][0]['file_path'], 'cast' : castList}
    except HTTPError as e:
        return None

getShowPage("The sopranos")

#print(getShow("The Sopranos"))
# TODO Cast, images, videos?
# TODO Cleaning up and error handling
# Videos might be a bit janky, maybe just poster instead?

# IMAGES DOWN HERE
def size_str_to_int(x):
    return float("inf") if x == 'original' else int(x[1:])

def img(file_path):
    print("FP = " +file_path)
    # Currently downloads one image and returns the filename
    CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'

    url = CONFIG_PATTERN.format(key=tmdb.API_KEY)
    r = requests.get(url)
    config = r.json()
    base_url = config['images']['base_url']
    sizes = config['images']['poster_sizes']

    max_size = max(sizes, key=size_str_to_int)
    url = "{0}{1}{2}".format(base_url, max_size, file_path)

    r = requests.get(url)
    filetype = r.headers['content-type'].split('/')[-1]
    #filename = 'poster_{0}.{1}'.format(file_path,filetype)
    filename = '{}'.format(file_path.replace('/',''))
    with open("media/" + filename,'wb') as w:
        w.write(r.content)
    return filename

#print(getShowPage("The Sopranos"))