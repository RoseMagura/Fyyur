from datetime import datetime


def format_genres(genres):
  return genres.replace('{', '').replace('}', '').replace('"', '')

def format_string_to_date(str):
  return datetime.strptime(str, '%Y-%m-%dT%H:%M:%S.%fZ')