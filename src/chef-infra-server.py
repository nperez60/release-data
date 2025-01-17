import requests
from bs4 import BeautifulSoup
import json

def get_release_date(version):
    url = f"https://github.com/chef/chef-server/releases/tag/{version}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        date_element = soup.find("relative-time", class_="no-wrap")
        if date_element:
            return date_element["datetime"][:10]
    return "N/A"

url = "https://docs.chef.io/release_notes_server/"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    h2_elements = soup.find_all('h2', text=lambda text: "Chef Infra Server" in text)
    
    releases = {}
    for h2_element in h2_elements:
        version_id = h2_element.get('id')
        release_date = get_release_date(version_id)
        releases[version_id] = release_date
    
    print(json.dumps(releases, indent=4, sort_keys=True))
else:
    print(f"Status code: {response.status_code}")
