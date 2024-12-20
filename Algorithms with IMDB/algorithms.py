import csv

PWD = '/Users/mebiuscat/Downloads/movies.csv'

with open('../data/movies.csv', newline='', encoding="UTF-8") as data:
    file_reader = csv.reader(data)

    moviedb = {}
    for line in file_reader:
        movie, rating = line
        moviedb[movie] = float(rating)
        if float(rating) == 6.0:
            print(f'{line[0]} - {line[1]}')
