import csv

with open('../data/movies.csv', newline='', encoding="UTF-8") as data:
    file_reader = csv.reader(data)

    moviedb = {}
    for line in file_reader:
        moviedb[line[0]] = line[1]
        print(f'{line[0]} - {line[1]}')

