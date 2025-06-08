from django.shortcuts import render
from django.http import JsonResponse
from .kaggle_loader import carregar_transacoes

# Create your views here.
from django.http import JsonResponse
from .kaggle_loader import carregar_transacoes, baixar_e_carregar_dataset
import networkx as nx
from analytics.models import Tabela, Dependencia
import plotly.graph_objects as go

def eda_basico(request):
    df = carregar_transacoes()
    info = {
        "linhas_colunas": df.shape,
        "colunas": df.columns.tolist(),
        "tipos": df.dtypes.astype(str).to_dict(),
        "nulos": df.isnull().sum().to_dict(),
        "exemplo": df.head(5).to_dict(orient="records")
    }
    return JsonResponse(info)

def dataset_resumo(request):
    data = baixar_e_carregar_dataset()
    resumo = {
        'transactions_shape': list(data['transactions'].shape),
        'transactions_columns': list(data['transactions'].columns),
        'transactions_head': data['transactions'].to_dict(orient='records'),
    }
    return JsonResponse(resumo)

def grafo_dependencias(request):
    # Construir grafo
    G = nx.DiGraph()

    tabelas = Tabela.objects.all()
    for t in tabelas:
        G.add_node(t.nome)

    dependencias = Dependencia.objects.all()
    for d in dependencias:
        G.add_edge(d.tabela_origem.nome, d.tabela_dependente.nome)

    # Layout do grafo
    pos = nx.spring_layout(G, k=0.5, iterations=50)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color='#1f78b4',
            size=20,
            line_width=2
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Grafo de Dependências entre Tabelas',
                        title_x=0.5,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    ))

    graph_html = fig.to_html(full_html=False)

    return render(request, 'analytics/grafo.html', {'graph_html': graph_html})


