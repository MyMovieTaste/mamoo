# 영화정보를 API를 이용해서 가져오기

# 홈페이지  https://www.themoviedb.org/
# Document  https://developers.themoviedb.org/3

import json
from pprint import pprint
# pip install requests
import requests
from tmdb import TMDBHelper

tmdb_helper = TMDBHelper('a7a15875c1c12251bc2930bc181baca0')
result = []
for page in range(1, 10):
    request_url=tmdb_helper.get_request_url(method='/movie/top_rated', region='KR', language='ko', page=f'{page}')
    raw_data = requests.get(request_url).json()
    data = raw_data.get('results')
    # pprint(data)
    for movie in data:
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
            }
        }
        result.append(movie_dict)

with open('top_rated.json', 'w', encoding="UTF-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

## genre
data = [
  {
    "model": "movies.genre",
    "pk": 28,
    "fields": {
      "name": "액션"
    }
  },
  {
    "model": "movies.genre",
    "pk": 12,
    "fields": {
      "name": "모험"
    }
  },
  {
    "model": "movies.genre",
    "pk": 16,
    "fields": {
      "name": "애니메이션"
    }
  },
  {
    "model": "movies.genre",
    "pk": 35,
    "fields": {
      "name": "코미디"
    }
  },
  {
    "model": "movies.genre",
    "pk": 80,
    "fields": {
      "name": "범죄"
    }
  },
  {
    "model": "movies.genre",
    "pk": 99,
    "fields": {
      "name": "다큐멘터리"
    }
  },
  {
    "model": "movies.genre",
    "pk": 18,
    "fields": {
      "name": "드라마"
    }
  },
  {
    "model": "movies.genre",
    "pk": 10751,
    "fields": {
      "name": "가족"
    }
  },
  {
    "model": "movies.genre",
    "pk": 14,
    "fields": {
      "name": "판타지"
    }
  },
  {
    "model": "movies.genre",
    "pk": 36,
    "fields": {
      "name": "역사"
    }
  },
  {
    "model": "movies.genre",
    "pk": 27,
    "fields": {
      "name": "공포"
    }
  },
  {
    "model": "movies.genre",
    "pk": 10402,
    "fields": {
      "name": "음악"
    }
  },
  {
    "model": "movies.genre",
    "pk": 9648,
    "fields": {
      "name": "미스터리"
    }
  },
  {
    "model": "movies.genre",
    "pk": 10749,
    "fields": {
      "name": "로맨스"
    }
  },
  {
    "model": "movies.genre",
    "pk": 878,
    "fields": {
      "name": "SF"
    }
  },
  {
    "model": "movies.genre",
    "pk": 10770,
    "fields": {
      "name": "TV 영화"
    }
  },
  {
    "model": "movies.genre",
    "pk": 53,
    "fields": {
      "name": "스릴러"
    }
  },
  {
    "model": "movies.genre",
    "pk": 10752,
    "fields": {
      "name": "전쟁"
    }
  },
  {
    "model": "movies.genre",
    "pk": 37,
    "fields": {
      "name": "서부"
    }
  },
]

result = []
for genre in data:
    fields = genre.get("fields")
    genre_dict = {
        "model" : genre.get("model"),
        "pk" : genre.get("pk"),
        "fields" : {
            "name" : fields.get("name")
        }
    }
    result.append(genre_dict)

with open('genres.json', 'w', encoding="UTF-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)