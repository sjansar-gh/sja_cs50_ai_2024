import csv
import sys
from collections import deque

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # people:  { '102': {'name': 'Kevin Bacon', 'birth': '1958', 'movies': {}}, ...} 
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            # names: { 'kevin bacon': {'102'}, ...}
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"]) # if more actors have same name 

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # movies:  { '112384': {'title': 'Apollo 13', 'year': '1995', 'stars': {}}, . . .}
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # It reads person_id and movie_id from each row and add in people's movies set
        # It reads movie_id & person_id from each row and add in movies's stars set 
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "small" #"large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # print('names: ', names)
    # print('people: ', people)
    # print('movies: ', movies)

    # Takes first actor name as input and get person id from names collection
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    
    # Takes 2nd actor name as input and get person id from names collection
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print('path: ', path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.
    If no possible path, returns None.
    """
    # Fetch ids of the source and target actors
    # Using BFS to find the shortest path
    frontier = deque([])
    # frontier.add(Node(state=source, parent=None, action=None))
    frontier.appendleft(Node(state=source, parent=None, action=None))

    # Set of explored ids to avoid duplicate elements
    explored = set()

    while True:
        if len(frontier) == 0:
            print("No connection found")
            # raise Exception("No solution")
            return None

        # print('frontier: ')
        # frontier.print()

        node = frontier.pop()

        if node.state == target:
            path = []

            while node.parent is not None:
                path.append((node.action, node.state))
                node = node.parent
            path.reverse()
            return path

        explored.add((node.action, node.state))

        neighbors = neighbors_for_person(node.state)
        if bool(neighbors):
            for action, state in neighbors:
                print('action=', action, ', state: ', state)
                if not contains_state(frontier, state) and (action, state) not in explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.appendleft(child)
        else:
            print("No co-actors found for ", node.state)
            return None

def contains_state(dq, state):
    return any(node.state == state for node in dq)

def person_id_for_name(name):
    """ Returns person id from names collection. """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]

def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]: 
            neighbors.add((movie_id, person_id))
    print('neighbors: ', neighbors)
    return neighbors


if __name__ == "__main__":
    main()
