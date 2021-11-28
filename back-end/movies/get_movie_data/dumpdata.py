# 영화정보를 API를 이용해서 가져오기

# 홈페이지  https://www.themoviedb.org/
# Document  https://developers.themoviedb.org/3

import json
from pprint import pprint
# pip install requests
import requests
from tmdb import TMDBHelper

tmdb_helper = TMDBHelper('a7a15875c1c12251bc2930bc181baca0')


def get_top_rated():
  result = []
  ranking = 0
  for page in range(1, 10):
    request_url=tmdb_helper.get_request_url(method='/movie/top_rated', region='KR', language='ko', page=f'{page}')
    raw_data = requests.get(request_url).json()
    data = raw_data.get('results')
    for movie in data:
        ranking += 1
        movie_dict = {
            "model" : "movies.movie",
            "pk" : movie.get("id"),
            "fields" : {
                "title" : movie.get("title"),
                "overview" : movie.get("overview"),
                "popularity" : movie.get("popularity"),
                "vote_count" : movie.get("vote_count"),
                "vote_average" : movie.get("vote_average"),
                "release_date" : movie.get("release_date"),
                "poster_path" : movie.get("poster_path"),                
                "genre_ids" : movie.get("genre_ids"),
                "year" : int(movie.get("release_date")[:4]),
                "ranking" : ranking,
            }
        }
        result.append(movie_dict)
  return result

with open('../fixtures/top_rated.json', 'w', encoding="UTF-8") as f:
  json.dump(get_top_rated(), f, ensure_ascii=False, indent=2)
