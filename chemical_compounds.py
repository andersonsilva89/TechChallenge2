import numpy as np
import random
import pygame
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# constantes do ga 
POPULATION_SIZE = 20
N_GENERATIONS = 200 
MUTATION_PROBABILITY = 0.2
N_COMPOUNDS = 10
COMPOUND_ATTRIBUTES = 3

# constantes do pygame
WIDTH, HEIGHT = 800, 800
INFO_HEIGHT = 300
PLOT_HEIGHT = 400
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NODE_RADIUS = 10
FONT_SIZE = 18

# inicializa o pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("algoritmo genético - teste de compostos")
font = pygame.font.SysFont('Arial', FONT_SIZE)
clock = pygame.time.Clock()

# função para gerar uma população aleatória de compostos
def generate_random_population():
    return [np.random.rand(N_COMPOUNDS, COMPOUND_ATTRIBUTES) for _ in range(POPULATION_SIZE)]

# função para calcular a fitness de um composto
def calculate_fitness(compound):
    efficacy = np.sum(compound[:, 0])
    toxicity = np.sum(compound[:, 1])
    bioavailability = np.sum(compound[:, 2])
    return efficacy / (toxicity + 1)  # evita divisão por zero

# função para ordenar a população com base no fitness
def sort_population(population):
    fitness_values = [calculate_fitness(individual) for individual in population]
    population = [x for _, x in sorted(zip(fitness_values, population), key=lambda pair: pair[0], reverse=True)]
    return population, sorted(fitness_values, reverse=True)

# função para realizar crossover entre dois pais - (OnePoint Crossover)
def crossover(parent1, parent2):
    crossover_point = random.randint(1, N_COMPOUNDS - 1)
    child = np.vstack((parent1[:crossover_point], parent2[crossover_point:]))
    return child

# função para realizar crossover entre dois pais - (TwoPoint Crossover)
def crossover_two_point(parent1, parent2):
    point1 = random.randint(1, N_COMPOUNDS - 2)
    point2 = random.randint(point1 + 1, N_COMPOUNDS - 1)
    child = np.vstack((parent1[:point1], parent2[point1:point2], parent1[point2:]))
    return child

# função para mutar um composto
def mutate(compound):
    if random.random() < MUTATION_PROBABILITY:
        mutation_point = random.randint(0, N_COMPOUNDS - 1)
        compound[mutation_point] = np.random.rand(COMPOUND_ATTRIBUTES)
    return compound

# função para exibir detalhes do composto no pygame
def display_compound(screen, compound):
    for i, attributes in enumerate(compound):
        text = font.render(f"composto {i+1}: eficácia={attributes[0]:.2f}, toxicidade={attributes[1]:.2f}, bioacessibilidade={attributes[2]:.2f}", True, BLACK)
        screen.blit(text, (10, 30 * i + 10))

# função para desenhar o gráfico de fitness usando matplotlib e depois blitar para o pygame
def draw_plot(screen, generations, fitness_values):
    fig, ax = plt.subplots(figsize=(6, 3))  # ajusta o tamanho da figura para caber na janela do pygame
    ax.plot(generations, fitness_values, color='blue')
    ax.set_xlabel('geração')
    ax.set_ylabel('fitness')
    ax.set_title('fitness ao longo das gerações')
    
    canvas = FigureCanvas(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.buffer_rgba()
    size = canvas.get_width_height()

    plot_surface = pygame.image.frombuffer(raw_data, size, 'RGBA')
    plot_surface = pygame.transform.scale(plot_surface, (WIDTH, PLOT_HEIGHT))
    screen.blit(plot_surface, (0, INFO_HEIGHT))

    plt.close(fig)

# função principal do ga
def genetic_algorithm():
    population = generate_random_population()
    best_fitness_values = []
    best_compound = None
    for generation in range(N_GENERATIONS):
        population, fitness_values = sort_population(population)
        best_fitness_values.append(fitness_values[0])
        best_compound = population[0]
        
        #new_population = [population[0]]  # elitismo: mantém o melhor indivíduo
        new_population = []  # elitismo: mantém o melhor indivíduo
        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = random.choices(population[:10], k=2)
            child = crossover_two_point(parent1, parent2)
            child = mutate(child)
            new_population.append(child)
        
        population = new_population

        # saída no console para acompanhar o progresso
        print(f"geração {generation}: melhor fitness = {fitness_values[0]:.2f}")
        print(f"melhor composto: {best_compound}")

        yield generation, best_fitness_values, best_compound

# inicializa o ga
ga_generator = genetic_algorithm()

# loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
        generation, best_fitness_values, best_individual = next(ga_generator)
    except StopIteration:
        running = False
        break

    screen.fill(WHITE)
    display_compound(screen, best_individual)
    draw_plot(screen, list(range(len(best_fitness_values))), best_fitness_values)
    pygame.display.flip()
    clock.tick(FPS)

# saída final para o melhor resultado
print("melhor composto final:")
for i, attributes in enumerate(best_individual):
    print(f"composto {i+1}: eficácia={attributes[0]:.3f}, toxicidade={attributes[1]:.3f}, bioacessibilidade={attributes[2]:.3f}")

# fecha o pygame
pygame.quit()
sys.exit()
