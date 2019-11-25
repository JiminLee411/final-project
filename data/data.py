import requests
from decouple import config
import csv
import pprint

api_key = config('API_KEY')

with open('boxoffice.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('movie_id', 'movie_title',)
    csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    csv_writer.writeheader()
    movieList = []
    movieKoTitle = []
    for page in range(1,450):
        api_url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=ko-KR&page={page}'
        response = requests.get(api_url).json()

        for movie in range(20):
            infos = response['results'][movie]
            if infos['id'] not in movieList:
                movieList.append(infos['id'])
                movieKoTitle.append([infos['id'], infos['title']])
                csv_writer.writerow({
                                    'movie_id': infos['id'],
                                    'movie_title': infos['title']
                                    })

# movie detail data
movieInfos = {}
movieGenres = {}
actors = []

for movie in range(len(movieList)):
    api_url = f'https://api.themoviedb.org/3/movie/{movieList[movie]}?api_key={api_key}&language=ko-KR'
    response = requests.get(api_url).json()
    movieDetail = response
    movieInfos[movieList[movie]] = {
        'id': movieList[movie],
        'adult': response['adult'] if response['adult'] else None,
        'budget': response['budget'] if response['budget'] else None,
        'genres': None,
        'original_title': response['original_title'] if response['original_title'] else None,
        'overview': response['overview'] if response['overview'] else None,
        'popularity': response['popularity'] if response['popularity'] else None,
        'poster_path': response['poster_path'] if response['poster_path'] else None,
        'release_date': response['poster_path'] if response['poster_path'] else None,
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
        movieInfos[movieList[movie]]['genres'] = response['genres'][genre]['id']

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
                movieInfos[movieList[movie]][f'actor_{actorIndex+1}'] = actorInfo[actorIndex]['id']
                            
    if crewInfo:
        for crew in crewInfo:
            if crew['job'] == 'Director':
                movieInfos[movieList[movie]]['director'] = crew['name']

    api_url = f'https://api.themoviedb.org/3/movie/{movieList[movie]}/images?api_key={api_key}'         
    response = requests.get(api_url).json()
    imgInfo = response['backdrops']

    val = 3 if len(imgInfo) >= 3 else len(imgInfo)

    for imgIndex in range(val):
        movieInfos[movieList[movie]][f'file_path_{imgIndex+1}'] = imgInfo[imgIndex]['file_path']

with open('movie.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('id','adult', 'budget', 'genres', 'original_title', 'overview', 'popularity', 'poster_path', 'release_date', 'revenue', 'runtime', 'tagline', 'title', 'vote_average', 'actor_1', 'actor_2', 'actor_3', 'actor_4', 'actor_5', 'director', 'file_path_1', 'file_path_2', 'file_path_3')
    csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    csv_writer.writeheader()
    for item in movieInfos.values():
        csv_writer.writerow(item)

# genre Information
for genreIndex in range(19):
    api_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=ko-KR'
    response = requests.get(api_url).json()
    genreInfo = response['genres'][genreIndex]
    movieGenres[genreInfo['id']] = {
        'name': genreInfo['name'],
        'genre_id': genreInfo['id']
    }
with open('genres.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('id','name','genre_id')
    csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    csv_writer.writeheader()
    for item in movieGenres.values():
        csv_writer.writerow(item)

# Actor list
with open('actor_list.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('id','actor_id','actor_name')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    ccount = 0
    for actorIndex in range(len(actors)):
        ccount += 1
        writer.writerow({'id' : ccount,
            'actor_id' : actors[actorIndex]['actor_id'],
            'actor_name' : actors[actorIndex]['actor_name']})