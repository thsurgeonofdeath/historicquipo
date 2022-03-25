from collections import namedtuple
from random import choices, randrange, random
from typing import List, Tuple
from django.contrib.gis.geoip2 import GeoIP2
import json
import requests




def get_lat_lng(position):
    # Recuperer latitude et longitude de chaque position
    parameters = {
        "key": "2aowAuUYcqE4qGGgSkFc7jAI182TqaGw",
        "location": position
    }
    response = requests.get("http://www.mapquestapi.com/geocoding/v1/address", params=parameters)
    data = json.loads(response.text)['results']
    lat = data[0]['locations'][0]['latLng']['lat']
    lng = data[0]['locations'][0]['latLng']['lng']
    return lat, lng


# centrer la carte de sorte qu'on voit les deux destinations
# latB=lonB=None car au début on aura pas de destination
def arrange_map(latA, lonA, latB=None, lonB=None):
    coordinates = (latA, lonA)
    if latB:
        coordinates = [(latA + latB) / 2, (lonA + lonB) / 2]
    return coordinates


def get_zoom(distance):
    if distance <= 100:
        return 10
    elif 100 < distance <= 500:
        return 7
    elif 500 < distance <= 2000:
        return 5
    elif 2000 < distance <= 5000:
        return 4
    else:
        return 2


def alg_Approximatif(loc1, loc2, loc3, loc4):
    lat1, lng1 = get_lat_lng(loc1)
    lat2, lng2 = get_lat_lng(loc2)
    lat3, lng3 = get_lat_lng(loc3)
    lat4, lng4 = get_lat_lng(loc4)
    Thing = namedtuple('thing', ['name', 'value', 'weight'])
    things = [
        Thing('location1', lat1, lng1),
        Thing('location2', lat2, lng2),
        Thing('location3', lat3, lng3),
        Thing('location4', lat4, lng4)
    ]
    Genome = List[int]
    Population = List[Genome]
    FitnessFunc = callable[[Genome], int]
    PopulateFunc = callable[[], Population]
    SelectionFunc = callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
    CrossoverFunc = callable[[Genome, Genome], Tuple[Genome, Genome]]
    MutationFunc = callable[[Genome], Genome]

    def generate_genome(length: int) -> Genome:
        return choices([0, 1], k=length)

    def generate_population(size: int, genome_length: int) -> Population:
        return [generate_genome(genome_length) for _ in range(size)]

    def fitness(genome: Genome, things: [Thing], weight_limit: int) -> int:
        if len(genome) != len(things):
            raise ValueError("genome and things must be of the same length")
        weight = 0
        value = 0
        for i, thing in enumerate(things):
            if genome[i] == 1:
                weight += thing.weigth
                value += thing.value

                if weight > weight_limit:
                    return 0
        return value

    def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
        return choices(
            population=population,
            weights=[fitness_func(genome) for genome in population],
            k=2
        )

    def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
        if len(a) != len(b):
            raise ValueError("Genomes a and b must be of same length")
            length = len(a)
            if length < 2:
                return a, b
            p = randint(1, length - 1)
        return a[0:p] + b[p:], b[0:p] + a[p:]

    def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
        for _ in range(num):
            index = randrange(len(genome))
            genome[index] = genome[index] if random() > probability else abs(genome[index] - 1)
        return genome

    def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
        for _ in range(num):
            index = randrange(len(genome))
            genome[index] = genome[index] if random() > probability else abs(genome[index] - 1)
        return genome

    def run_evolution(
            population_func: PopulateFunc,
            fitness_func: FitnessFunc,
            fitness_limit: int,
            selection_func: SelectionFunc = selection_pair,
            crossover_func: CrossoverFunc = single_point_crossover,
            mutation_func: MutationFunc = mutation,
            generation_limit: int = 100
    ) -> Tuple[Population, int]:
        population = population_func()
        for i in range(generation_limit):
            population = sorted(
                population,
                key=lambda genome: fitness_func(genome),
                reverse=True

            )

            if fitness_func(population[0]) >= fitness_limit:
                break

        next_generation = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]

        population = next_generation
        population = sorted(
            population,
            key=lambda genome: fitness_func(genome),
            reverse=True
        )
        return population, i

        start = time.time()
        population, generations = run_evolution(
            population_func=partial(
                generate_population, size=10, genome_length=len(things)
            ),
            fitness_func=partial(
                fitness, things=things, weight_limit=3000
            ),
            fitness_limit=1310,
            generation_limit=100
        )
        end = time.time()

        def genome_to_things(genome: Genome, things: [Thing]) -> [Thing]:
            result = []
            for i, thing in enumerate(things):
                if genome[i] == 1:
                    result += [thing.name]

        # resultat
        print(f"number of generations :{generations}")
        print(f"time : (end-start)s")
        print(f"best solution: {genome_to_things(population[0], things)}")
