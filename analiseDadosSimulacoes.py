import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

filename = 'simulacoes_atual.csv'
df = pd.read_csv(filename)

def plot_frequencies(df):
    fig = go.Figure()

    unique_simulations = df['simulation_id'].unique()
    for simulation_id in unique_simulations:
        subset = df[df['simulation_id'] == simulation_id]
        fig.add_trace(go.Scatter(
            x=subset['generation'],
            y=subset['frequency_of_mutants'],
            mode='lines',
            name=f'Simulação {simulation_id}',
            hovertext=f'Taxa de Mutação: {subset["mutation_rate"].iloc[0]}',
            hoverinfo='text'
        ))

    fig.update_layout(
        title='Evolução da Frequência de Mutantes nas Simulações',
        xaxis_title='Geração',
        yaxis_title='Frequência de Mutantes'
    )

    fig.show()

def plot_mean_std(df):
    grouped = df.groupby('generation')['frequency_of_mutants'].agg(['mean', 'std']).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=grouped['generation'],
        y=grouped['mean'],
        mode='lines',
        name='Média'
    ))
    fig.add_trace(go.Scatter(
        x=grouped['generation'],
        y=grouped['mean'] + grouped['std'],
        mode='lines',
        name='Média + Desvio Padrão',
        line=dict(dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=grouped['generation'],
        y=grouped['mean'] - grouped['std'],
        mode='lines',
        name='Média - Desvio Padrão',
        line=dict(dash='dash')
    ))

    fig.update_layout(
        title='Média e Desvio Padrão da Frequência de Mutantes ao Longo das Gerações',
        xaxis_title='Geração',
        yaxis_title='Frequência de Mutantes'
    )

    fig.show()

plot_frequencies(df)
plot_mean_std(df)
