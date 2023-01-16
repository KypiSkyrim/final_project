import pandas as pd
import typing
from typing import Any
import csv
import matplotlib.pyplot as plt


#0
def date_change(str_date: str) -> str:
  """Функция перевода даты в формат через точку."""
  day_month = str_date.replace(' ', '.')
  month_year = day_month.replace('.20', '.19')
  date = month_year.replace('.19', '.')
  return date


def form(df: Any) -> str:
  """Функция запроса и вывода даты в определенном формате из файла .csv."""
  number = int(input ('Введите ранг песни: '))-1
  str_date = str(df.loc[number, 'Release Date'])
  result_date = date_change(str_date)
  return print(result_date)


df = pd.read_csv('spotify_songs_top_100.csv')
form(df)


assert date_change('19 January.18') == '19.January.18'
assert date_change('19 January 2018') == '19.January.18'
assert date_change('19.January 2018') == '19.January.18'
assert date_change('19.January.2018') == '19.January.18'
assert date_change('19 January 1918') == '19.January.18'
assert date_change('19.January 1918') == '19.January.18'
assert date_change('19.January.1918') == '19.January.18'


#1.1
def ed_sheeran_song(df: Any) -> Any:
  """Функция создания файла с песнями, автор которых Ed Sheeran, на основе файла .csv"""
  artist = df[df['Artist'].str.contains(r'Ed Sheeran')]
  artist.to_json('Song.json') 


df = pd.read_csv('spotify_songs_top_100.csv')
ed_sheeran_song(df)


#1.2
def the_oldest(df: Any) -> Any:
  """Функция создания файла с самыми старыми песнями на основе файла .csv"""
  df["datetime"] = pd.to_datetime(df['Release Date'], dayfirst=True)
  df = df.sort_values("datetime").drop(columns="datetime")
  df = df.reset_index(drop=True)
  release = df.loc[:2, ["Release Date", "Song"]]
  release.to_json('Release Date.json') 


df = pd.read_csv('spotify_songs_top_100.csv')
the_oldest(df)


#1.3
def convert_streams(streams: str) -> float:
  """Функция перевода строк в числа с плавающей точкой в файле .csv"""
  new_streams = streams.replace(',', '.')
  return float(new_streams)


def summation(df: Any) -> Any:
  """Функция создания файла с суммой прослушиванийй всех песен для каждого автора на основе файла .csv"""
  df['Streams (Billions)'] = df['Streams (Billions)'].apply(convert_streams)
  streams = df.groupby('Artist')['Streams (Billions)'].sum()
  streams.to_json('Streams (Billions).json')


df = pd.read_csv('spotify_songs_top_100.csv')
summation(df)


#2
def histogram(df: Any) -> Any:
  """Функция создания файла .png с гистограммой количества песен по годам на основе файла .csv"""
  df["Release Date"] = pd.to_datetime(df['Release Date'], dayfirst=True)
  bins = lambda x: x.max().year - x.min().year
  plt.hist(df['Release Date'],
          label="All songs", 
          bins=bins(df['Release Date']), 
          color='green', 
          alpha=0.7)
  plt.title('Top songs by year')
  plt.xlabel('Songs')
  plt.ylabel('Number of songs')
  plt.legend()
  plt.grid(True)
  plt.savefig('Top_songs_by_year.png')
  plt.show


df = pd.read_csv('spotify_songs_top_100.csv')
histogram(df)
