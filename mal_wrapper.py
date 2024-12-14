import requests
import pandas as pd


class MalWrapper:
    def __init__(self, mal_client_id: str):
        self.anime_fields = {
            "id": "MAL identifier",
            "title": "Title of the anime",
            "synopsis": "Anime synopsis",
            "mean": "The mean score of the anime",
            "rank": "The rank of the anime based on the mean score",
            "popularity": "Popularity score",
            "nsfw": "Whether it is safe for work or not",
            "genres": "Array of objects (Genre)",
            "media_type": "What type of media it is (OVA, special, etc.)",
            "status": "Airing status.",
            "list_status": "User information",
            "num_episodes": "The total number of episodes of this series. If unknown, it is 0.",
            "start_season": "Which season it started airing",
            "source": "Type of anime",
            "average_episode_duration": "",
            "rating": "The age rating of the anime",
            "studios": "Array of objects (AnimeStudio)"
        }

        self.headers = {
            'X-MAL-CLIENT-ID': mal_client_id
        }

    def fetch_data(self, url, headers=None):
        try:
            response = requests.get(url, headers=self.headers if headers is None else headers)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()  # Assume API returns JSON data
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return {"data": []}

    def retrieve_mal_list_for_user(self, mal_user_id: str, result_limit: int = 1000, return_raw_json: bool = True):

        user_anime_list_url = f"https://api.myanimelist.net/v2/users/{mal_user_id}/animelist?sort=list_score&" \
                              f"limit={result_limit}&" \
                              f"fields={str(list(self.anime_fields.keys()))}"

        anime_list_json_response = self.fetch_data(user_anime_list_url)

        if return_raw_json:
            return anime_list_json_response
        else:
            return pd.json_normalize(anime_list_json_response["data"],)

