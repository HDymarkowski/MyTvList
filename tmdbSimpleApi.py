from PIL import Image
from requests.models import HTTPError
# This is the one I'm going to use, launch from anaconda navigator for the right virtual enviroment
import tmdbsimple as tmdb
import requests
from tmdbsimple import search

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

def getIdPerson(person):
    try:
        search = tmdb.Search()
        personId = search.person(query=person)['results'][0]['id']
        return personId
    except HTTPError as e:
        # Maybe deal with this better
        print("Show does not exist")
        print("({})".format(e))
        # ALT-OUTPUT empty list
        return None


def getRecommendations(show):
    # Returns top 8 (if possible) reccomendations of the show inputted
    # List of dictionaries containing 'title', 'tagline' and 'poster_path'
    try:
        recs = []
        showId = getId(show)
        #showId = show

        reccomendations = tmdb.TV.recommendations(tmdb.TV(showId))
        reccomendedShows = reccomendations['results']
        noReccomedations = reccomendations['total_results']

        for i in range(min(8, noReccomedations)):
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
        print("Show does not exist")
        print("({})".format(e))
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
            print("Show does not exist")
            print("({})".format(e))
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



# print(getCastMemberPage(getIdPerson("James Gandolfini")))

"""
img = Image.open("http://image.tmdb.org/tv" + tmdb.TV.images(tmdb.TV(1))['posters'][0]['file_path'])
img.show
"""

#print(getShow("The Sopranos"))
# TODO Cast, images, videos?
# TODO Cleaning up and error handling
# Videos might be a bit janky, maybe just poster instead?
