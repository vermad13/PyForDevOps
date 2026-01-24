
import requests

url = "https://api.github.com/users/octocat/repos"
response = requests.get(url)

if response.status_code == 200:
    repos = response.json()
    print("Repos:")
    for repo in repos:
        print(f"- {repo['name']}")
else:
    print("Failed to fetch data", response.status_code)
