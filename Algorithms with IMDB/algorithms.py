import csv

with open('../data/movies.csv', newline='', encoding="UTF-8") as data:
    file_reader = csv.reader(data)

    moviedb = []
    for line in file_reader:
        movie, rating = line
        moviedb.append((movie, float(rating)))


for i in range(len(moviedb) - 1):
    offset = 0
    for j in range(offset + 1, len(moviedb)):
        if moviedb[offset][1] > moviedb[j][1]:
            moviedb[offset], moviedb[j] = moviedb[j], moviedb[offset]
        offset = j

for movie, rating in moviedb:
    print(f'{movie} - {rating}')