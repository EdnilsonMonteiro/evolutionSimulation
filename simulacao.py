import numpy as np
import pandas as pd
import os
import random
import time

# Função de reprodução com seleção natural
def reproduce(population, mutation_rate, selection_pressure):
    next_generation = []
    fitness = np.where(population == 1, 1 + selection_pressure, 1 - selection_pressure)
    probabilities = fitness / fitness.sum()
    for _ in range(len(population) // 2):
        parent1 = np.random.choice(population, p=probabilities)
        parent2 = np.random.choice(population, p=probabilities)
        child1 = parent1 if np.random.random() > mutation_rate else 1 - parent1
        child2 = parent2 if np.random.random() > mutation_rate else 1 - parent2
        next_generation.extend([child1, child2])
    return np.array(next_generation)

# Função para executar uma simulação
def run_simulation(simulation_id, num_individuals, num_generations, mutation_rate, selection_pressure, list_id):
    population = np.zeros(num_individuals)
    data = {'list_id': [], 'simulation_id': [], 'generation': [], 'frequency_of_mutants': [], 'num_individuals': [], 'num_generations': [], 'mutation_rate': [], 'selection_pressure': []}
    for generation in range(num_generations):
        frequency_of_mutants = np.mean(population)
        data['list_id'].append(list_id)
        data['simulation_id'].append(simulation_id)
        data['generation'].append(generation)
        data['frequency_of_mutants'].append(frequency_of_mutants)
        data['num_individuals'].append(num_individuals)
        data['num_generations'].append(num_generations)
        data['mutation_rate'].append(mutation_rate)
        data['selection_pressure'].append(selection_pressure)
        population = reproduce(population, mutation_rate, selection_pressure)
    return pd.DataFrame(data)

# Parâmetros para simulações aleatórias
def generate_parameters():
    num_individuals = 2000
    num_generations = 300
    mutation_rate = random.uniform(0.2, 0.3)
    selection_pressure = random.uniform(-0.1, 0.1)  # Seleção natural variando entre -0.1 e 0.1
    return num_individuals, num_generations, mutation_rate, selection_pressure

# Verificar se o arquivo CSV já existe e determinar o próximo simulation_id
filename_all = 'todas_simulacoes_evolucao.csv'
filename_current_list = 'simulacoes_atual.csv'
filename_list_index = 'lista_simulacoes.csv'

if os.path.exists(filename_all) and os.path.getsize(filename_all) > 0:
    df_existing = pd.read_csv(filename_all)
    last_simulation_id = df_existing['simulation_id'].max()
else:
    last_simulation_id = 0

if os.path.exists(filename_list_index) and os.path.getsize(filename_list_index) > 0:
    df_list_existing = pd.read_csv(filename_list_index)
    last_list_id = df_list_existing['list_id'].max()
else:
    last_list_id = 0

# Incrementar o ID da lista de simulações
current_list_id = last_list_id + 1

# Executar simulações e armazenar resultados
df_all_simulations = pd.DataFrame()
df_current_list_simulations = pd.DataFrame()
num_simulations = 5

start_time = time.time()

for i in range(num_simulations):
    simulation_id = last_simulation_id + i + 1
    num_individuals, num_generations, mutation_rate, selection_pressure = generate_parameters()
    df_simulation = run_simulation(simulation_id, num_individuals, num_generations, mutation_rate, selection_pressure, current_list_id)
    df_all_simulations = pd.concat([df_all_simulations, df_simulation], ignore_index=True)
    df_current_list_simulations = pd.concat([df_current_list_simulations, df_simulation], ignore_index=True)

end_time = time.time()

# Salvar os dados (existentes e novos) em um arquivo CSV
if os.path.exists(filename_all) and os.path.getsize(filename_all) > 0:
    df_all_simulations.to_csv(filename_all, mode='a', header=False, index=False)
else:
    df_all_simulations.to_csv(filename_all, index=False)

# Salvar a lista atual de simulações em um CSV separado
df_current_list_simulations.to_csv(filename_current_list, index=False)

# Atualizar o índice de listas de simulações
df_list_entry = pd.DataFrame({'list_id': [current_list_id], 'num_simulations': [num_simulations], 'timestamp': [time.ctime()]})
if os.path.exists(filename_list_index) and os.path.getsize(filename_list_index) > 0:
    df_list_entry.to_csv(filename_list_index, mode='a', header=False, index=False)
else:
    df_list_entry.to_csv(filename_list_index, index=False)

# Calcular o tempo total
total_time = end_time - start_time
print(f'Tempo total para {num_simulations} simulações: {total_time:.2f} segundos')
