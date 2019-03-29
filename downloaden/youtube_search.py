#!/usr/bin/python

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = 'AIzaSyA3p4BIDGqjrOxnJSJAWf1NKke6UMnv7o8'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(query = "choose query", maxResults = 5):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=query,
    part='id, snippet',
    maxResults=maxResults
  ).execute()

  videos = dict()

  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      title = search_result['snippet']['title']
      url_id = search_result['id']['videoId']
      url = 'https://www.youtube.com/watch?v={}'.format(url_id)

      videos[title] = url

  return videos 

videos = youtube_search("hoi")
print(videos)