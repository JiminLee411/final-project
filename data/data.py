import requests
from decouple import config
import csv
import pprint

api_key = config('API_KEY')

movieList = []
movieDict = {}

# boxoffice
for page in range(1,36):
    # 인기순
    api_url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=ko-KR&page={page}'
    response = requests.get(api_url).json()
    # 평점순
    api_url2 = f'https://api.themoviedb.org/3/movie/top_rated?api_key={api_key}&language=ko-KR&page={page}'
    response2 = requests.get(api_url2).json()

    for movie in range(20):
        popularInfo = response['results'][movie]
        topRateInfo = response2['results'][movie]

        if popularInfo['id'] not in movieList:
            movieList.append(popularInfo['id'])
            movieDict[popularInfo['id']] = {
                'movie_id': popularInfo['id'],
                'movie_title': popularInfo['title']
            }

    for movie in range(20):    
        if topRateInfo['id'] not in movieList:
            movieList.append(topRateInfo['id'])
            movieDict[topRateInfo['id']] = {
                'movie_id': topRateInfo['id'],
                'movie_title': topRateInfo['title']
            }

with open('data/boxoffice.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('movie_id', 'movie_title',)
    csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    csv_writer.writeheader()
    
    for item in movieDict.values():
        csv_writer.writerow(item)


# movie detail data
movieInfos = {}
movieGenres = {}
actors = []

cnt = 1
for movie in range(len(movieList)):
    api_url = f'https://api.themoviedb.org/3/movie/{movieList[movie]}?api_key={api_key}&language=ko-KR'
    response = requests.get(api_url).json()
    movieDetail = response
    movieInfos[cnt] = {
        'id': cnt,
        'adult': response['adult'] if response['adult'] else None,
        'budget': response['budget'] if response['budget'] else None,
        'genres': None,
        'original_title': response['original_title'] if response['original_title'] else None,
        'overview': response['overview'] if response['overview'] else None,
        'popularity': response['popularity'] if response['popularity'] else None,
        'poster_path': response['poster_path'] if response['poster_path'] else None,
        'release_date': response['release_date'] if response['release_date'] else None,
        'revenue': response['revenue'] if response['revenue'] else None,
        'runtime': response['runtime'] if response['runtime'] else None,
        'tagline': response['tagline'] if response['tagline'] else None,
        'title': response['title'] if response['title'] else None,
        'vote_average': response['vote_average'] if response['vote_average'] else None,
        'actor_1': None,
        'actor_2': None,
        'actor_3': None,
        'actor_4': None,
        'actor_5': None,
        'director': None,
        'file_path_1': None,
        'file_path_2': None,
        'file_path_3': None,
    }
    
    for genre in range(len(response['genres'])):
        movieInfos[cnt]['genres'] = response['genres'][genre]['id']

    api_url = f'https://api.themoviedb.org/3/movie/{movieList[movie]}/credits?api_key={api_key}'
    response = requests.get(api_url).json()

    actorInfo = response['cast']
    crewInfo = response['crew']

    if actorInfo:
        val = 5 if len(actorInfo) >= 5 else len(actorInfo)
        for actorIndex in range(val):
            if actorInfo[actorIndex]['id'] not in actors:
                actors.append({
                        'actor_id': actorInfo[actorIndex]['id'],
                        'actor_name': actorInfo[actorIndex]['name']
                    })
                movieInfos[cnt][f'actor_{actorIndex+1}'] = actorInfo[actorIndex]['id']
                            
    if crewInfo:
        for crew in crewInfo:
            if crew['job'] == 'Director':
                movieInfos[cnt]['director'] = crew['name']

    api_url = f'https://api.themoviedb.org/3/movie/{movieList[movie]}/images?api_key={api_key}'         
    response = requests.get(api_url).json()
    imgInfo = response['backdrops']

    val = 3 if len(imgInfo) >= 3 else len(imgInfo)

    for imgIndex in range(val):
        movieInfos[cnt][f'file_path_{imgIndex+1}'] = imgInfo[imgIndex]['file_path']

    cnt += 1

with open('data/movie.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('id','adult', 'budget', 'genres', 'original_title', 'overview', 'popularity', 'poster_path', 'release_date', 'revenue', 'runtime', 'tagline', 'title', 'vote_average', 'actor_1', 'actor_2', 'actor_3', 'actor_4', 'actor_5', 'director', 'file_path_1', 'file_path_2', 'file_path_3')
    csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    csv_writer.writeheader()
    for item in movieInfos.values():
        csv_writer.writerow(item)


# genre Information
id = 0
for genreIndex in range(19):
    api_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=ko-KR'
    response = requests.get(api_url).json()
    genreInfo = response['genres'][genreIndex]
    movieGenres[genreInfo['id']] = {
        'id': id,
        'name': genreInfo['name'],
        'genre_id': genreInfo['id']
    }
    id += 1

with open('data/genres.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('id','name','genre_id')
    csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    csv_writer.writeheader()
    for item in movieGenres.values():
        csv_writer.writerow(item)

# Actor list
with open('data/actor_list.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('id','actor_id','actor_name')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    ccount = 0
    for actorIndex in range(len(actors)):
        ccount += 1
        writer.writerow({'id' : ccount,
            'actor_id' : actors[actorIndex]['actor_id'],
            'actor_name' : actors[actorIndex]['actor_name']})