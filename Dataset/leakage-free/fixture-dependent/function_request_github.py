import requests


def get_github_repo(stars_threshold=1000, per_page=3):

    if not isinstance(stars_threshold, int) or stars_threshold <= 0:
        raise ValueError("Error: stars_threshold should be a positive integer.")
    if not isinstance(per_page, int) or per_page <= 0:
        raise ValueError("Error: per_page should be a positive integer.")

    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"language:python stars:>={stars_threshold}",
        "sort": "stars",
        "order": "desc",
        "per_page": per_page
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        repos = []
        for item in response.json()["items"]:
            repos.append({
                "name": item["name"],
                "stars": item["stargazers_count"],
                "url": item["html_url"]
            })
        return repos
    except (requests.RequestException, KeyError):
        return None

get_github_repo()