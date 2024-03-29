language: python
python:
  - "3.5"
install:
  - pip install requests

import json
import requests
"""
Program: The program is a function that will communicate using the RESTful services APIs provided by GitHub. The GitHub APIs will
         allow you to query for information about users and their repositories,

AUTHOR:   Ogadinma Njoku

PURPOSE:  A graduate course assignment for Software Testing
"""


def user_api_commits(username):
    try:
        res = requests.get('https://api.github.com/users/%s/repos' % username)
    except urllib.error.HTTPError as e:
        print('HTTPError:{}'.format(e.code))
    except urllib.error.URLError as e:
        print('URLError: {}'.format(e.reason))
    else:
        print('OK!')
        repos = json.loads(res.content)

    for repo in repos:
        if repo['fork'] is True: continue
        num = count_repo_commits(repo['url'] + '/commits')
        repo['num_commits'] = num
        yield repo


def count_repo_commits(commits_url, account=0):
    res = requests.get(commits_url)
    commits = json.loads(res.content)
    num = len(commits)
    if num == 0:
        return account
    link = res.headers.get('link')
    if link is None:
        return account + num
    second_url = find_second(r.headers['link'])
    if second_url is None:
        return account + num
    # Iteratively recurse the function result
    return count_repo_commits(second_url, account + num)


# Find a second link for Github API 
def find_second(link):
    for line in link.split(','):
        aline, bline = line.split(';')
        if bline.strip() == 'rel="next"':
            return aline.strip()[1:-1]


if __name__ == '__main__':

    try:
        username = input('Enter the User : ')
        print("Repositories in user's Github API Interface  ")
    except IndexError:
        print ( "Usage: %s <username>" % username)
        
    for repo in user_api_commits(username):
        print ("Repo: %(name)s Number %(num_commits)d  of commits." % repo)
        
language: python
python:
  - "3.5"
install:
  - pip install requests
