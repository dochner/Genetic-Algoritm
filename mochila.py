# -*- coding: utf-8 -*-
from operator import itemgetter

GENERATION_PORCENTAGE = 100
GENERATION_TIMES = 5
MAX_WEIGHT = 30

items = [
    {"name": "Saco de dormir", "weight": 15, "points": 15},
    {"name": "Corda", "weight": 3, "points": 7},
    {"name": "Canivete", "weight": 2, "points": 10},
    {"name": "Tocha", "weight": 5, "points": 5},
    {"name": "Garrafa", "weight": 9, "points": 8},
    {"name": "Comida", "weight": 20, "points": 17}
]

population = [
    {"chooses": [1, 0, 0, 1, 1, 0], "score": 0, "totalweight": 0},
    {"chooses": [0, 0, 1, 1, 1, 0], "score": 0, "totalweight": 0},
    {"chooses": [0, 1, 0, 1, 0, 0], "score": 0, "totalweight": 0},
    {"chooses": [0, 1, 1, 0, 0, 1], "score": 0, "totalweight": 0}
]


def setScoreAndTotalWeight(population):
    filteredGenerations = []

    for pop in population:
        alreadyCalculated = pop["score"] > 0 or pop["totalweight"] > 0
        if alreadyCalculated:
            filteredGenerations.append(pop)
            continue

        for i, choose in enumerate(pop["chooses"]):
            if choose:
                item = items[i]
                pop["score"] += item["points"]
                pop["totalweight"] += item["weight"]

        filteredGenerations.append(pop)

    return filteredGenerations


def getParents(population):
    population.sort(key=lambda pop: pop["score"], reverse=True)
    return population[:(len(population) * GENERATION_PORCENTAGE) // 100]


def getChildrens(parents):
    childrens = []

    for i in range(len(parents)):
        childrens.append({"chooses": [], "score": 0, "totalweight": 0})
        childrens[-1]["chooses"].extend(list(itemgetter(*[0, 2, 4])
                                             (parents[i-1]["chooses"])))
        childrens[-1]["chooses"].extend(list(itemgetter(*[1, 3, 5])
                                             (parents[i]["chooses"])))

        childrens.append({"chooses": [], "score": 0, "totalweight": 0})
        childrens[-1]["chooses"].extend(list(itemgetter(*[1, 3, 5])
                                             (parents[i-1]["chooses"])))
        childrens[-1]["chooses"].extend(list(itemgetter(*[0, 2, 4])
                                             (parents[i]["chooses"])))

        childrens.append({"chooses": [], "score": 0, "totalweight": 0})
        childrens[-1]["chooses"].extend(list(itemgetter(*[0, 1, 2])
                                             (parents[i-1]["chooses"])))
        childrens[-1]["chooses"].extend(list(itemgetter(*[3, 4, 5])
                                             (parents[i]["chooses"])))

        childrens.append({"chooses": [], "score": 0, "totalweight": 0})
        childrens[-1]["chooses"].extend(list(itemgetter(*[3, 4, 5])
                                             (parents[i-1]["chooses"])))
        childrens[-1]["chooses"].extend(list(itemgetter(*[0, 1, 2])
                                             (parents[i]["chooses"])))

    childrens = setScoreAndTotalWeight(childrens)
    return childrens


def getBestOne(population):
    population = list(
        filter(lambda pop: pop["totalweight"] <= MAX_WEIGHT, population))

    if len(population):
        population.sort(
            key=lambda pop: pop["score"], reverse=True)
    else:
        return []

    return population[0]


population = setScoreAndTotalWeight(population)
for time in range(GENERATION_TIMES):
    parents = getParents(population)
    childrens = getChildrens(parents)
    print("Numero de gerações totais: " + str(len(population)) + " >> Pais gerados: " +
          str(len(parents)) + " >> Filhos gerados: " + str(len(childrens)))
    population.extend(childrens)

bestOne = getBestOne(population)
print()
print("De " + str(len(population)) + ", o melhor é: ")
print("Score: " + str(bestOne["score"]), end=', ')
print("Total weight: " + str(bestOne["totalweight"]))
print("Items: ", end='')

itemsName = [items[i]["name"]
             for i, choose in enumerate(bestOne["chooses"]) if choose]
print(itemsName)
