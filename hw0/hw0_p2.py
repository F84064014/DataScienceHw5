import random
import copy
import re
from typing import Callable

'''
my Series object which can return bool list with comparison operator
'''
class food:

    def __init__(self, name: str, lst: list) -> None:

        self._name = name
        self._data = lst

    def __getitem__(self, i: int):
        return self._data[i]

    def __len__(self) -> int:
        return len(self._data)

    def __eq__(self, obj) -> list:
        return [d == obj for d in self._data]

    def __ne__(self, obj) -> list:
        return [not x for x in self.__eq__(obj)]

    def __ge__(self, obj) -> list:
        return [d >= obj for d in self._data]

    def __gt__(self, obj) -> list:
        return [d > obj for d in self._data]

    def __le__(self, obj) -> list:
        return [d <= obj for d in self._data]

    def __lt__(self, obj) -> list:
        return [d < obj for d in self._data]

    def __repr__(self) -> str:
        return '\n'.join(['Name\n--------'] + [self._name, '--------'] + [str(d) for d in self._data] + ['--------'])

    def __contrains__(self, key) -> bool:
        return key in self._data

    def apply(self, funct: Callable) -> list:
        return [funct(data) for data in self._data]

    # def __str__(self) -> str:
    #     return [d for d in self._data]

    def unique(self) -> list:
        return set(list(self._data))

class ubereats:

    '''
    missing value
    '''
    nan = 'NaN'

    '''
    if you dont have pandas, then why dont you build one yourself?
        _data = list of dictionary
        _key  = name columns
    '''
    def __init__(self, data: list, columns: list) -> None:
        
        for i in range(len(data)):
            for j in range(len(columns)):
                # fill missing value with 'NaN'
                if data[i][j] == '' : data[i][j] = 'NaN' 

        self._data = [dict(zip(columns, d)) for d in data]
        self._keys = columns

    '''
    read_csv from path and turn into a ubereats dataframe
    '''
    def read_csv(path: str = '') -> None:

        data = []

        with open(path, 'r') as f:
            columns = [l.strip() for l in f.readline().split(',')]
            columns = [l.replace(re.search(r"\([^()]*\)", l).group() if re.search(r"\([^()]*\)", l) else '', '').strip() for l in columns]
            for line in f.readlines():
                temp = [l.strip() for l in line.split(',')]
                temp = [float(t) if t.replace('.', '').isdigit() else t for t in temp]
                data.append(temp)

        return ubereats(data, columns)

    '''
    n: int -> get largest n
    column: str -> the column selected
    find the row with largest n value in seleted column
    '''
    def nlargest(self, n: int = 3, column: str = '') -> 'ubereats':
        return ubereats([list(d.values()) for d in sorted(self._data, key=lambda x: x[column], reverse=True)[:n]], self._keys)

    '''
    get all column names
    '''
    def keys(self) -> None:
        return self._keys

    '''
    loop over each row by index and row
    '''
    def iterrows(self):
        for i in range(len(self._data)):
            yield (i, self._data[i])

    '''
    length of object
    '''
    def __len__(self) -> int:
        return len(self._data)

    '''
    key: str -> get single columns
    key: [str] -> select columns and return new dataframe
    key: [bool] -> select rows at True and return new dataframe
    '''
    def __getitem__(self, key):

        if isinstance(key, str):
            if key in self._keys:
                return food(key ,[x[key] for x in self._data])
            else:
                raise KeyError('invalid key \"{}\"'.format(key))
        elif isinstance(key, list):
            if  isinstance(key[0], bool):
                return ubereats([list(d.values()) for d, selected in zip(self._data, key) if selected], self._keys)
            elif isinstance(key[0], str):
                return ubereats([[d[k] for k in key] for d in self._data], key)
            else:
                raise KeyError('invalid key')

    '''
    set new attribute
    '''
    def __setitem__(self, key: str, value: list):
        for idx in range(len(self._data)):
            self._data[idx][key] = value[idx]
        if not key in self._keys:
            self._keys.append(key)

    '''
    representation
    '''
    def __repr__(self) -> str:
        
        return '\n'.join(['\t'.join(self._keys)] + ['\t'.join([str(val) for val in d.values()]) for d in self._data])

    '''
    n: int -> show n rows
    shuffle: bool -> randomly select row or not
    '''
    def head(self, n: int = 5, shuffle: bool = True) -> None:
        n = min(n, self.__len__())
        
        print('\t'.join(self._keys))

        selected = random.sample(list(range(len(self._data))), n) if shuffle else [i for i in range(n)]
        for i in selected:
            print('\t'.join([str(val) for val in self._data[i].values()]))

def problem1(df):

    # select data of 2016
    df_2016 = df[df['Year'] == 2016]
    # print top3 largest of rating and select tiltle and rating only
    print(df_2016.nlargest(3, 'Rating')[['Title', 'Rating']])

def problem2(df):

    actors = set()
    for _actors in df['Actors']:
        for actor in _actors:
            actors.add(actor)
    actors = list(actors)
    actors = dict(zip(actors, [[] for i in range(len(actors))]))

    # get dictionary which save Actors as key and list of Revenue as value
    df_AR = df[['Actors', 'Revenue']]
    for i, row in df_AR.iterrows():
        for actor in row['Actors']:
            if row['Revenue'] != ubereats.nan: actors[actor].append(row['Revenue'])

    # turn the value into average
    for key in actors.keys():
        # this happened when the only occurrance have NaN Revenue
        if len(actors[key])  == 0:
            actors[key] = 0
        else:
            actors[key] = (sum(actors[key])/len(actors[key]))

    print(sorted(actors.items(), key=lambda x: x[1], reverse=True)[0:2])
    # print('note1: Daisy Ridley also have the same average revenue')

def problem3(df):
    # save all rating where Emma Watson attend
    ratings = [row['Rating'] for i, row in df.iterrows() if 'Emma Watson' in row['Actors']]
    print(sum(ratings)/len(ratings))

def problem4(df):

    # get dictionary where keys is director and value is set of actors who collaberate with the director
    directors = df['Director'].unique()
    directors = dict(zip(directors, [set() for i in range(len(directors))]))
    for i, row in df.iterrows():
        for actor in row['Actors']:
            directors[row['Director']].add(actor)
    # sort by the number of actors and print
    for _ in sorted(directors.items(), key=lambda x: len(x[1]), reverse=True)[:3]:
        print(_[0], ':', len(_[1]))

    for _ in sorted(directors.items(), key=lambda x: len(x[1]), reverse=True)[3:]:
        if len(_[1]) == len(sorted(directors.items(), key=lambda x: len(x[1]), reverse=True)[3][1]):
            print(_[0], ':', len(_[1]))
        else:
            break

def problem5(df):

    actors = set()
    for _actors in df['Actors']:
        for actor in _actors:
            actors.add(actor)
    actors = list(actors)

    # reuse the actors in problem2
    actors = dict(zip(actors, [set() for i in range(len(actors))]))

    # dictionary actro as key and set of genre as value
    for i, row in df.iterrows():
        for actor in row['Actors']:
            for genre in row['Genre']:
                actors[actor].add(genre)

    # sort by number of genre and print
    for _ in sorted(actors.items(), key=lambda x: len(x[1]), reverse=True)[:2]:
        print(_[0], len(_[1]))
        # print()

    for _ in sorted(actors.items(), key=lambda x: len(x[1]), reverse=True)[2:]:
        if len(_[1]) == len(sorted(actors.items(), key=lambda x: len(x[1]), reverse=True)[1][1]):
            print(_[0], len(_[1]))
            # print()
        else:
            break

def problem6(df):
    actors = set()
    for _actors in df['Actors']:
        for actor in _actors:
            actors.add(actor)
    actors = list(actors)
    actors = dict(zip(actors, [(0,0) for i in range(len(actors))]))

    # update the min and max Year 
    def update_gap_year(gap: tuple, new: int) -> tuple:
        if gap == (0,0):
            return (new, new)
        else:
            return (min(gap[0], new), max(gap[1], new))

    # update year for all actors
    for i, row in df.iterrows():
        for actor in row['Actors']:
            actors[actor] = update_gap_year(actors[actor], row['Year'])

    # sort by difference in gap year and print
    for actor, years in actors.items():
        if years[1] - years[0] == 10:
            print(actor)

def problem7(df):

    actors = set()
    for _actors in df['Actors']:
        for actor in _actors:
            actors.add(actor)
    actors = list(actors)

    relations = dict(zip(actors, [[] for i in range(len(actors))]))

    # get dictionary with actor as key and list of directly related actor as value
    for i, row in df.iterrows():
        for actor in row['Actors']:
            relations[actor] += [_actor for _actor in row['Actors'] if not _actor == actor and not _actor in relations[actor]]

    Johnny_friends = []
    stack = copy.deepcopy(relations['Johnny Depp'])
    # DFS algorithm
    while stack:
        old_friend = stack.pop()
        if not old_friend in Johnny_friends:
            Johnny_friends.append(old_friend)
        for new_friend in relations[old_friend]:
            # if friend haven't been counted add to the stack, else pass
            if not new_friend in Johnny_friends and not new_friend in stack:
                stack.append(new_friend)

    print(len(Johnny_friends) if not 'Johnny Depp' in Johnny_friends else len(Johnny_friends)-1)
    print([actor for actor in Johnny_friends if actor != 'Johnny Depp'])
    # print(len(list(set(Johnny_friends))))



problems = [
    'Top-3 movies with the highest ratings in 2016?',
    'The actor generating the highest average revenue?',
    'The average rating of Emma Watson\'s movies?',
    'Top-3 directors who collaborate with the most actors?',
    'Top-2 actors playing in the most genres of movies?',
    'ALL actors whose movies lead to the largest maximum gap of years?',
    'find all actors who collaborate with Johnny Depp in direct and indirect ways?'
]

if __name__ == '__main__':

    df = ubereats.read_csv(r'IMDB-Movie-Data.csv')
    # turn Actors and Genre into list type
    df['Actors'] = df['Actors'].apply(lambda x: [x.strip() for x in x.split('|')])
    df['Genre'] = df['Genre'].apply(lambda x: [x.strip() for x in x.split('|')])
    # df.head()

    print('################problem1################')
    print(problems[0])
    problem1(df)

    print('################problem2################')
    print(problems[1])
    problem2(df)


    print('################problem3################')
    print(problems[2])
    problem3(df)

    print('################problem4################')
    print(problems[3])
    problem4(df)

    print('################problem5################')
    print(problems[4])
    problem5(df)
    

    print('###################problem6################')
    print(problems[5])
    problem6(df)

 
    print('###################problem7################')
    print(problems[6])
    problem7(df)
