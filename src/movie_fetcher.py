import requests
import re
import csv
from bs4 import BeautifulSoup

#Method to extract movie details
def read_data(list, movies, links, crew, ratings, votes):
    for index in range(0, len(movies)):
        # Separating movie into: 'place',
        # 'title', 'year'
        movie_string = movies[index].get_text()
        movie = (' '.join(movie_string.split()).replace('.', ''))
        movie_title = movie[len(str(index)) + 1:-7]
        year = re.search('\((.*?)\)', movie_string).group(1)
        place = movie[:len(str(index)) - (len(movie))]

        data = {"movie_title": movie_title,
                "year": year,
                "place": place,
                "star_cast": crew[index],
                "rating": ratings[index],
                "vote": votes[index],
                "link": links[index],
                "preference_key": index % 4 + 1}
        list.append(data)
    return list

#Method to write to CSV Values the details
#D - Dependency inversion: fields can be whatever and list can contain whatever so it is abstracted and not set to movies exclusively
def write_CSV(list, fields):
    with open("movie_results.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for movie in list:
            writer.writerow({**movie})

#Main sets variables and hub for functions 
#S - Single responsibility: because each method does just one thing one reads and one writes
#O - Open ended principle: main is open to extension as it just works as hub for other components
def main():
    # Downloading imdb top 250 movie's data
    url = 'http://www.imdb.com/chart/top'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    movies = soup.select('td.titleColumn')
    links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
    crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
    ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
    votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]

    # create a empty list for storing
    # movie information
    list = []
    fields = ["preference_key", "movie_title", "star_cast", "rating", "year", "place", "vote", "link"]

    # Iterating over movies to extract
    # each movie's details
    list = read_data(list, movies, links, crew, ratings, votes)

    #Method writes CSV file with data from the list and fields
    write_CSV(list, fields)


if __name__ == '__main__':
    main()
