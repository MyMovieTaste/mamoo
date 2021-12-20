# 영화정보를 API를 이용해서 가져오기

# 홈페이지  https://www.themoviedb.org/
# Document  https://developers.themoviedb.org/3

import json
from pprint import pprint
import requests
from tmdb import TMDBHelper
from pathlib import Path

# 시크릿키
import os, json
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent.parent
secret_file = os.path.join(BASE_DIR, 'api_key.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

tmdb_helper = TMDBHelper(get_secret("API_KEY"))

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


def get_year():
  result = []
  for year in range(1950, 2022):
    year_dict = {
        "model" : "movies.year",
        "pk" : year,
        "fields" : {
            "year_str" : str(year),
        }
    }
    result.append(year_dict)
  return result    

with open('../fixtures/year.json', 'w', encoding="UTF-8") as f:
  json.dump(get_year(), f, ensure_ascii=False, indent=2)