### Algoritmo Genético para Teste de Compostos: Documentação

#### Descrição do Problema

O objetivo deste projeto é encontrar a melhor combinação de compostos químicos que tenham a maior eficácia no tratamento de uma doença enquanto minimizam os efeitos colaterais. A abordagem do algoritmo genético (GA) é utilizada para otimizar o processo de seleção desses compostos com base em sua eficácia, toxicidade e bioacessibilidade.

#### Visão Geral do Algoritmo Genético

Um algoritmo genético é uma técnica de otimização inspirada pelo processo de seleção natural. Ele utiliza uma população de soluções potenciais que evoluem ao longo de gerações, melhorando as soluções com base em uma função de aptidão definida. As principais etapas em um algoritmo genético são:

1. **Inicialização**: Gerar uma população inicial de soluções aleatoriamente.
2. **Seleção**: Selecionar as melhores soluções com base em sua aptidão.
3. **Crossover**: Combinar pares de soluções para criar novos descendentes.
4. **Mutação**: Alterar aleatoriamente algumas soluções para manter a diversidade genética.
5. **Substituição**: Formar uma nova população substituindo algumas das soluções antigas por novas.
6. **Término**: Repetir o processo por um número definido de gerações ou até a convergência.

#### Explicação do Código

Aqui está uma explicação detalhada de como o código implementa o algoritmo genético para o teste de compostos:

##### Constantes e Inicialização

- **Constantes do GA**:
  - `POPULATION_SIZE`: Número de compostos na população.
  - `N_GENERATIONS`: Número de gerações para evoluir.
  - `MUTATION_PROBABILITY`: Probabilidade de mutação nos descendentes.
  - `N_COMPOUNDS`: Número de compostos sendo otimizados.
  - `COMPOUND_ATTRIBUTES`: Número de atributos para cada composto (eficácia, toxicidade, bioacessibilidade).

- **Constantes do Pygame**:
  - Várias configurações para a exibição do Pygame, incluindo tamanho da janela, cores, tamanho da fonte, etc.

##### Inicialização do Pygame

- `pygame.init()`: Inicializa o Pygame.
- `screen = pygame.display.set_mode((WIDTH, HEIGHT))`: Configura a janela de exibição.
- `pygame.display.set_caption("Algoritmo Genético - Teste de Compostos")`: Define o título da janela.
- `font = pygame.font.SysFont('Arial', FONT_SIZE)`: Inicializa a fonte para renderização de texto.
- `clock = pygame.time.Clock()`: Inicializa o relógio para controlar a taxa de quadros.

##### Definições das Funções

1. **Gerando População Aleatória**:
    ```python
    def generate_random_population():
        return [np.random.rand(N_COMPOUNDS, COMPOUND_ATTRIBUTES) for _ in range(POPULATION_SIZE)]
    ```
    Esta função cria uma população inicial de compostos aleatórios com atributos entre 0 e 1.

2. **Calculando a Aptidão**:
    ```python
    def calculate_fitness(compound):
        efficacy = np.sum(compound[:, 0])
        toxicity = np.sum(compound[:, 1])
        bioavailability = np.sum(compound[:, 2])
        return efficacy / (toxicity + 1)  # evita divisão por zero
    ```
    A aptidão é calculada como a razão entre a eficácia total e a toxicidade total mais um (para evitar divisão por zero). Maior eficácia e menor toxicidade melhoram a aptidão.

3. **Ordenando a População**:
    ```python
    def sort_population(population):
        fitness_values = [calculate_fitness(individual) for individual in population]
        population = [x for _, x in sorted(zip(fitness_values, population), key=lambda pair: pair[0], reverse=True)]
        return population, sorted(fitness_values, reverse=True)
    ```
    Esta função ordena a população com base nos valores de aptidão em ordem decrescente.

4. **Crossover de Ponto Único**:
    ```python
    def crossover(parent1, parent2):
        crossover_point = random.randint(1, N_COMPOUNDS - 1)
        child = np.vstack((parent1[:crossover_point], parent2[crossover_point:]))
        return child
    ```

5. **Crossover de Dois Pontos**:
    ```python
    def crossover_two_point(parent1, parent2):
        point1 = random.randint(1, N_COMPOUNDS - 2)
        point2 = random.randint(point1 + 1, N_COMPOUNDS - 1)
        child = np.vstack((parent1[:point1], parent2[point1:point2], parent1[point2:]))
        return child
    ```
    Cria um descendente combinando partes de dois pais em pontos de crossover escolhidos aleatoriamente.

6. **Mutação**:
    ```python
    def mutate(compound):
        if random.random() < MUTATION_PROBABILITY:
            mutation_point = random.randint(0, N_COMPOUNDS - 1)
            compound[mutation_point] = np.random.rand(COMPOUND_ATTRIBUTES)
        return compound
    ```
    Introduz alterações aleatórias em um descendente com uma certa probabilidade para manter a diversidade.

7. **Exibindo Compostos**:
    ```python
    def display_compound(screen, compound):
        for i, attributes in enumerate(compound):
            text = font.render(f"composto {i+1}: eficácia={attributes[0]:.2f}, toxicidade={attributes[1]:.2f}, bioacessibilidade={attributes[2]:.2f}", True, BLACK)
            screen.blit(text, (10, 30 * i + 10))
    ```
    Renderiza os detalhes dos compostos na tela do Pygame.

8. **Desenhando o Gráfico de Aptidão**:
    ```python
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
    ```

##### Função Principal do Algoritmo Genético

```python
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
```

Esta função executa o algoritmo genético por um número especificado de gerações. Inicializa uma população, avalia a aptidão, seleciona os melhores indivíduos, realiza crossover e mutação, e substitui a população antiga por novos indivíduos. Imprime o progresso no console e retorna a geração atual, os melhores valores de aptidão e o melhor composto.

##### Loop Principal

```python
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
```

Este é o loop principal do Pygame que mantém o programa em execução. Ele obtém a próxima geração do algoritmo genético, atualiza a tela com os melhores compostos e desenha o gráfico de aptidão.

#### Como Executar o Código

1. Certifique-se de ter Python e as bibliotecas necessárias instaladas (`numpy`, `pygame

`, `matplotlib`).
2. Copie o código em um arquivo Python.
3. Execute o arquivo Python.

O programa exibirá uma janela do Pygame com os compostos e suas aptidões, bem como um gráfico mostrando a evolução da aptidão ao longo das gerações.

#### Considerações Finais

Este código implementa um algoritmo genético básico para otimizar a seleção de compostos com base em eficácia, toxicidade e bioacessibilidade. A visualização com o Pygame permite acompanhar a evolução das soluções ao longo das gerações. Ajustes adicionais podem ser feitos para refinar os parâmetros do algoritmo e melhorar a performance e os resultados.