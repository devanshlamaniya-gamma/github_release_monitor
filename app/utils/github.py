import requests
from datetime import datetime , timedelta


def fetch_last_hour_commits(owner:str , repo : str , since : datetime , token : str = None):

    url = f"https://api.github.com/repos/{owner}/{repo}/commits"

    headers = {}

    if token:
        headers["Authorization"] = f"token {token}"

    params = {"since" : since.isoformat() + "Z"}

    response = requests.get(url ,headers=headers , params=params)

    if response.status_code != 200:
            raise Exception(f"github api error {response.status_code} : {response.text}")
    

    return response.json()

# owner = "chromium"
# repo_name = "chromium"
# since = datetime.utcnow() - timedelta(hours=3)
# token = None

# result = fetch_last_hour_commits(owner , repo_name , since , token)
# for c in result:
#     commit_name = c["commit"]["author"]["name"]
#     commit_email = c["commit"]["author"]["email"]
#     commit_time = c["commit"]["author"]["date"]
#     commit_message = c["commit"]["message"]

#     print("name of author : " ,commit_name)
#     print("email of author" , commit_email)
#     print("time of commit : " , commit_time)
#     print("commit message : " , commit_message)
