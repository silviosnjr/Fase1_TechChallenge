import pandas as pd
import numpy as np

# Número de registros
num_records = 21000

# Distribuição do IMC
imc_distribution = [
    {'interval': (17, 18.4), 'percentage': 0.05},
    {'interval': (18.5, 24.9), 'percentage': 0.30},
    {'interval': (25, 29.9), 'percentage': 0.32},
    {'interval': (30, 34.9), 'percentage': 0.15},
    {'interval': (35, 39.9), 'percentage': 0.09},
    {'interval': (40, 41), 'percentage': 0.06}
]

# Função para gerar IMC de acordo com a distribuição
def generate_imc():
    rand = np.random.random()
    cumulative = 0
    for dist in imc_distribution:
        cumulative += dist['percentage']
        if rand <= cumulative:
            return np.random.uniform(*dist['interval'])

# Gerar dados
data = {
    'IMC': [generate_imc() if np.random.random() < 0.999 else None for _ in range(num_records)],  # Introduzindo alguns valores nulos
    'idade': np.random.randint(0, 99, size=num_records),
    'genero': np.random.choice(['masculino', 'feminino'], size=num_records, p=[0.4, 0.6]),
    'fumante': np.random.choice(['sim', 'nao'], size=num_records, p=[0.2, 0.8]),
    'regiao': np.random.choice(['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'],
                               size=num_records, p=[0.05, 0.1, 0.15, 0.3, 0.4])
}

# Ajustar idade para IMC > 35
imc_array = np.array(data['IMC'])
is_imc_valid = imc_array >= 35
is_imc_null = pd.isnull(imc_array)
valid_indices = np.logical_and(is_imc_valid, ~is_imc_null)
data['idade'][valid_indices] = np.random.randint(0, 45, size=np.sum(valid_indices))

# Gerar número de filhos com base na idade
def generate_filhos(idade):
    if idade < 14:
        return 0
    elif idade <= 16:
        return np.random.randint(0, 2)
    elif idade <= 20:
        return np.random.randint(0, 4)
    elif idade <= 24:
        return np.random.randint(0, 6)
    elif idade <= 30:
        return np.random.randint(0, 9)
    elif idade <= 40:
        return np.random.randint(1, 11)
    else:
        return np.random.randint(1, 13)

data['filhos'] = [generate_filhos(idade) for idade in data['idade']]

# Gerar encargos com base na idade
data['encargos'] = data['idade'] * np.random.uniform(1000, 1500, size=num_records)

# Simular dados vazios em 'filhos'
empty_indices = np.random.choice(num_records, size=235, replace=False)
data['filhos'][empty_indices] = np.nan

# Criar DataFrame
df = pd.DataFrame(data)

# Salvar em um arquivo CSV
df.to_csv('dados_saude.csv', index=False)
