import csv

def bubble_sort(moviedb):
    for i in range(len(moviedb) - 1):
        offset = 0
        for j in range(offset + 1, len(moviedb)):
            if moviedb[offset][1] > moviedb[j][1]:
                moviedb[offset], moviedb[j] = moviedb[j], moviedb[offset]
            offset = j


def binary_search(moviedb, rating):
    low, high = 0, len(moviedb) - 1
    while low < high:
        mid = int((high + low) // 2)
        mrating = moviedb[mid][1]
        if mrating >= rating:
            high = mid - 1
        else:
            low = mid + 1

    while low < len(moviedb) and moviedb[low][1] == rating:
        movie, rating = moviedb[low]
        print(f'{movie} - {rating}')
        low += 1


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return merge(left_half, right_half)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i][1] < right[j][1]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result

with open('../data/movies.csv', newline='', encoding="UTF-8") as data:
    file_reader = csv.reader(data)

    moviedb = []
    for line in file_reader:
        movie, rating = line
        moviedb.append((movie, float(rating)))

    # bubble_sort(moviedb)
    moviedb = merge_sort(moviedb)
    binary_search(moviedb, 6.0)
