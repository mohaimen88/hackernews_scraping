import requests 
from bs4 import BeautifulSoup
import pprint
import sqlite3
from sqlite3 import Error
from datetime import datetime


res = requests.get('https://news.ycombinator.com/')
soup = BeautifulSoup(res.text, 'html.parser')

links = soup.select('.storylink')
subtext = soup.select('.subtext')

def sort_stories_by_votes(hn_list):
    return sorted(hn_list, key = lambda k:k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)



# Create Connection / Database (db will be created if it doesn't already exist)
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection



# Save data to db
def execure_save_query(connection, query, link, title, votes, date):
    cursor = connection.cursor()
    try:
        cursor.execute(query, (link, title, votes, date))
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


connection = create_connection('hn_app.sqlite')

# news is a dict with all the data we need 
news = create_custom_hn(links, subtext)
# print(news)

save_query = '''
        INSERT INTO 
            hn_news (link, title, votes, date)
        VALUES
            (?, ?, ?, ?)
'''
date = datetime.now()

for n in news:
    link = n['link']
    title = n['title']
    votes = n['votes']
    execure_save_query(connection, save_query, link, title, votes, date)



