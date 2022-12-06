import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pandas as pd
import json

def return_session(username, password):
    s = requests.Session()
    payload = {
        "utf8": "%E2%9C%93",
        "user[login]": username,
        "user[password]": password,
        "commit": "Log+In"
    }
    site = s.get("https://archiveofourown.org")
    soup = BeautifulSoup(site.content, 'html.parser')
    payload["authenticity_token"] = soup.find("input", {"name": "authenticity_token"})['value']

    s.encoding = 'utf-8'
    s.post("https://archiveofourown.org/users/login", data=payload)
    return s

def get_pages(base_url, session):
    request = session.get(base_url)
    soup = BeautifulSoup(request.content, 'html.parser')
    pages = soup.find("ol", { "class": "pagination actions" })
    all_pages = []
    for li in pages.findAll('li'):
        all_pages.append(li.text)
    max_pages = int(all_pages[-2])
    return [*range(1, max_pages+1)]

def get_fics(base_url, session):
    while True:
        request = session.get(base_url)
        if request.status_code == 200:
            break
        else:
            time.sleep(300)
            continue

    soup = BeautifulSoup(request.content, 'html.parser')
    works = soup.find("ol", { "class": "reading work index group" })
    all_fics = []
    fics = works.findChildren("li", recursive=False)
    for i in fics:
        try:
            temp_fic = fic_check(i)
            if temp_fic['dt'] >= datetime(2022, 1, 1, 0, 0):
                all_fics.append(temp_fic)
            else:
                break
        except:
            pass

    return all_fics

def fic_check(soup):
    title_array = []
    character_array = []
    freeform_array = []

    heading = soup.find("h4", { "class": "heading"})
    title_details = heading.findChildren("a", recursive=False)
    for i in title_details:
        title_array.append(i.text)
    try:
        relationships = soup.find("li", { "class": "relationships" }).text.replace('\n', '')
    except:
        relationships = "NONE"
    characters = soup.findAll("li", { "class": "characters" })
    for i in characters:
        character_array.append(i.text)

    freeforms = soup.findAll("li", { "class": "freeforms"})
    for i in freeforms:
        freeform_array.append(i.text)

    visited = soup.find("h4", { "class": "viewed heading" }).text.replace('\n', '').replace(',', '')
    visited_list = visited.split()
    visited_count = visited_list[visited_list.index("Visited") + 1]
    if visited_count == "once":
        visited_count = 1
    else:
        visited_count = int(visited_count)

    last_visited = (' ').join(visited_list[2:5])
    dt = datetime.strptime(last_visited, '%d %b %Y')

    word_count = int(soup.find("dd", { "class": "words"}).text.replace(',', ''))

    details = {
        "title": title_array[0],
        "author": title_array[1],
        "relationship": relationships,
        "characters": character_array,
        "word_count": word_count,
        "tags": freeform_array,
        "visited": visited_count,
        "dt": dt
    }
    return details


def load_data(username, password):
    session = return_session(username, password)
    base_url = f"https://archiveofourown.org/users/{username}/readings"
    all_pages = get_pages(base_url, session)
    all_fics = []
    all_breaks = []
    for i in all_pages:
        try:
            fics_url = base_url + f"?page={i}"
            fics = get_fics(fics_url, session)
            for fic in fics:
                all_fics.append(fic)
                if fic["dt"] >= datetime(2021, 1, 1):
                    all_breaks.append(False)
                else:
                    all_breaks.append(True)
            time.sleep(5)
        except:
            pass

        if True in all_breaks:
            print(f'BREAKING ON PAGE {i}')
            break

    return all_fics

def resolve_request(username, password):
    raw_data = load_data(username, password)
    frame = pd.DataFrame(raw_data)
    most_visited = frame[frame.visited == frame.visited.max()]

    total_words = frame.word_count.sum()
    total_fics = len(frame)
    total_reads = frame.visited.sum()

    all_relations = []
    all_characters = []
    all_tags = []

    for i in raw_data:
        all_relations.append(i["relationship"])
        for x in i["characters"]:
            all_characters.append(x)
        for x in i["tags"]:
            all_tags.append(x)

    relations_df = pd.DataFrame(all_relations)[0].value_counts().head(5).index.tolist()
    characters_df = pd.DataFrame(all_characters)[0].value_counts().head(5).index.tolist()
    tags_df = pd.DataFrame(all_tags)[0].value_counts().head(5).index.tolist()
    mv = {
        "title": most_visited.iloc[0].title,
        "author": most_visited.iloc[0].author,
        "count": int(most_visited.iloc[0].visited),
        "relations": relations_df,
        "characters": characters_df,
        "tags": tags_df
    }

    return_data = {
        "username": username,
        "total_words": int(total_words),
        "total_fics": int(total_fics),
        "total_reads": int(total_reads),
        "most_visited": mv,
    }
    return return_data
