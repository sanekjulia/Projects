import random
import math
import matplotlib.pyplot as plt
from IPython.display import clear_output

# wizualizacja jednego rozwiązania z trasą
def vizualize(cities_list, nr_gen):
    x_coords = [city.x for city in cities_list]
    y_coords = [city.y for city in cities_list]
    labels = [city.id for city in cities_list]

    plt.plot(x_coords + [x_coords[0]], y_coords + [y_coords[0]],  
            color='gray', linestyle='-', linewidth=1)
    plt.scatter(x_coords, y_coords, color='red')

    for i in range(len(cities_list)):
        plt.text(x_coords[i] + 2, y_coords[i] + 2, str(labels[i]), fontsize=9)

    plt.xlim(0, 310)
    plt.ylim(0, 310)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Aktualna trasa – Pokolenie nr: {nr_gen}', fontsize=12)
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')

    clear_output(wait=True)  # <- CZYŚCIMY POPRZEDNI OUTPUT
    plt.show()               # <- POKAZUJEMY NOWY
    plt.pause(0.3)           # <- NA CHWILĘ STOP (działa też w Jupyterze)

# obiekt City - atrybuty: indeks, wspolrzedne x, y
class City: 
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
    def __repr__(self):
        return f"{self.id}: ({self.x}, {self.y})"

# Funkcja generująca listę miast
def generate_cities(number_of_cities):
    cities_list = []

    for i in range(number_of_cities):
        x = random.randint(0, 300)
        y = random.randint(0, 300)
        id = i
        cities_list.append(City(id+1,x,y))
    return cities_list

# Funkcja celu obliczana dla pojedynczego rozwiązania - chromosomu
def fitness_function(chromosom):
    length_sum = 0
    for a, b in zip(chromosom, chromosom[1:] + [chromosom[0]]):  # trasa zamknięta
        dx = a.x - b.x
        dy = a.y - b.y
        length_sum += math.sqrt(dx**2 + dy**2)
    return length_sum


# Funkcja generująca populację początkową
def generate_population(cities_list,population_size):
    population = []
    for _ in range(population_size):
        chromosom = cities_list.copy()
        random.shuffle(chromosom)
        population.append(chromosom)
    return population

def crossover(chromosom1, chromosom2):
    index = random.randint(0, len(chromosom1) - 1) #losujemy index do krzyzowania
    child1 = chromosom1[0:index]
    child2 = chromosom2[0:index]
    for element in chromosom2:
        if element not in child1:
            child1.append(element)
    for element in chromosom1:
        if element not in child2:
            child2.append(element)
    return child1, child2

def mutation(chromosom, mutation_probability):
    if random.random() < mutation_probability:
        idx1 = random.randint(0, len(chromosom)-1)
        idx2 = random.randint(0, len(chromosom)-1)
        if idx1==idx2:
                idx2 = idx2-1 # zmniejszam o 1, w razie czego bedzie to ostatni element listy
        chromosom[idx1], chromosom[idx2] = chromosom[idx2], chromosom[idx1]
    return chromosom
    
def generate_new_population(population, population_size, probabilities, mutation_probability):
    temp_population = []
    for i in range(population_size // 2):
        parent1, parent2 = random.choices(population, weights=probabilities, k=2)
        child1, child2 = crossover(parent1, parent2)
        temp_population.extend([child1, child2])
    new_population = [mutation(chromosom, mutation_probability) for chromosom in temp_population]
    return new_population