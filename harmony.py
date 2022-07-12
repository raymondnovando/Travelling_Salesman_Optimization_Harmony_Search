import random
from util import City, read_cities, write_cities_and_return_them, generate_cities, path_cost, visualize_tsp, read_tsp
from scipy.spatial import distance_matrix
import matplotlib.pyplot as plt
from statistics import mean

def fitness(harmony):
    score = 0
    for i in range(dimension - 1):
        score = score + dist_matrix[harmony[i].get_index()][harmony[i + 1].get_index()]
    score = score + dist_matrix[harmony[0].get_index()][harmony[dimension - 1].get_index()]
    return score


def nearest_city(city, unvisited):
    if len(unvisited) > 0:
        nearest_city = min(unvisited, key=lambda x: x.distance(city))
        return nearest_city
    else:
        return None

def get_score(harmony):
    return harmony.get('score')

def random_route():
    return random.sample(cities, dimension)

def greedy_route(start_index):
        unvisited = cities[:]
        del unvisited[start_index]
        route = [cities[start_index]]
        while len(unvisited):
            index, nearest_city = min(enumerate(unvisited), key=lambda item: item[1].distance(route[-1]))
            route.append(nearest_city)
            del unvisited[index]
        return route
# define response variable
listfitness = []
cities = read_tsp("eil51.tsp")

listcity = []
for city in cities:
    listcity.append(city.get_list())
dist_matrix = distance_matrix(listcity, listcity, p=2)
bestcost = []

hmcr = .9
parmin = 0.35
parmax = 0.99
# par1 = .25
# par2 = .5
dimension = len(cities)
hms = 100
iterasi = 5000
for ii in range(30):
    print(ii)
    hm = []
    for i in range(hms):
        harmony = random_route()
        score = fitness(harmony)
        hm.append({"harmony": harmony, "score": score})

    # harmony = greedy_route(0)
    # score = fitness(harmony)
    # hm.append({"harmony": harmony, "score": score})
    hm.sort(key=get_score)
    # plt.ion()
    # plt.draw()
    for i in range(iterasi):
        new_harmony = []
        par = parmin + ((parmax-parmin)/iterasi)*i
        for j in range(dimension):
            if hmcr >= random.random():
                cities_in_memory = []
                for harmony in hm:
                    cities_in_memory.append(harmony["harmony"][j])
                cities_in_memory = [x for x in cities_in_memory if x not in new_harmony]
                if len(cities_in_memory) > 0:
                    nextcity = random.choice(cities_in_memory)
                else:
                    untraveled_cities = cities[:]
                    untraveled_cities = [x for x in untraveled_cities if x not in new_harmony]
                    nextcity = random.choice(untraveled_cities)
                randpar = random.random()
                par1 = par/2
                if randpar < par1:
                    if j > 0:
                        new_harmony[j-1], nextcity = nextcity, new_harmony[j-1]
                elif randpar < par:
                    if j > 0:
                        untraveled_cities = cities[:]
                        untraveled_cities = [x for x in untraveled_cities if x not in new_harmony]
                        parcity = nearest_city(new_harmony[j-1],untraveled_cities)
                        if parcity != None:
                            nextcity = parcity
            else:
                untraveled_cities = cities[:]
                untraveled_cities = [x for x in untraveled_cities if x not in new_harmony]
                nextcity = random.choice(untraveled_cities)
            new_harmony.append(nextcity)
        new_score = fitness(new_harmony)
        if new_score < hm[hms-1]["score"]:
            hm[hms-1]["harmony"] = new_harmony
            hm[hms-1]["score"] = new_score
            hm.sort(key=get_score)
        bestcost.append(hm[0]["score"])

        # if i % 20 == 0:
        #     plt.figure(0)
        #     plt.plot()
        #     plt.plot(bestcost, 'g')
        #     plt.ylabel('Distance')
        #     plt.xlabel('Generation')
        #     fig = plt.figure(0)
        #     fig.suptitle('HS iter')
        #     x_list, y_list = [], []
        #     for city in hm[0]["harmony"]:
        #         x_list.append(city.x)
        #         y_list.append(city.y)
        #     x_list.append(hm[0]["harmony"][0].x)
        #     y_list.append(hm[0]["harmony"][0].y)
        #     fig = plt.figure(1)
        #     fig.clear()
        #     fig.suptitle(f'HS TSP iter {i}')
        #     plt.plot(x_list, y_list, 'ro')
        #     plt.plot(x_list, y_list, 'g')
        #     plt.draw()
        #     plt.pause(.0001)
    # fig = plt.figure(1)
    # fig.suptitle('HS TSP')
    # print(hm[0]["score"])
    listfitness.append(hm[0]["score"])
# plt.plot(x_list, y_list, 'ro')
# plt.plot(x_list, y_list)
# plt.show(block=True)
print(listfitness)
print(mean(listfitness))
print(max(listfitness))
print(min(listfitness))