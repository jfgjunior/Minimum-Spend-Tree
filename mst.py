# -*- coding: utf-8 -*-
#nome: José Fernando Garcia Junior   email: jf.junior18@hotmail.com

import networkx as nx
import numpy as np
from sys import exit
from numpy import Inf
# importar o metodo que transforma uma lista em heap
from heapq import heapify
# importar o metodo que remove o elemento com menor prioridade do heap
from heapq import heappop as pop
# importar o metodo que insere um elemento no heap
from heapq import heappush as push

def main():
    '''
    Parametros: -
    Retorno:    -
    Função: Fazer as chamadas de manipulação das três árvores pedidas
    '''
    Op = int(raw_input('\nDigite:\n1 - Para grafo "Cidades da inglaterra"\n2 - Para grafo "Cidades da alemanha"\n3 - Para grafo "Cidades dos EUA"\n'))
    Op2 = int(raw_input('\nDigite:\n1 - Para criar comunidades\n2 - Para mostrar somente a MST\n'))
    if Op2 == 1:
        numero_vertices = int(raw_input('\nDigite o número de vértices para serem retirados\n'))

    if Op == 1:
        #Primeiro grafo
        grafo,dic_pesos = gera_grafo('cidades_inglaterra12.txt')
        nome = 'cidades_inglaterra12mst.png'
        arvore = Prim(grafo,dic_pesos)
        if Op2 == 1:
            nome = 'cidades_ingalterra_'+str(numero_vertices)+'.png'
            if numero_vertices <= nx.number_of_edges(arvore):
                arvore = retira_aresta(arvore,dic_pesos,numero_vertices)
            else:
                print 'Número de vertices a serem retirados não compatível'
                exit(0)
        arvore_comunidades = nx.to_agraph(arvore)
        arvore_comunidades.layout('dot', args='-Nfontsize=10 -Nwidth=".2" -Nheight=".2" -Nmargin=0 -Gfontsize=8')
        arvore_comunidades.draw(nome)
        print 'arquivo criado com o nome: ',nome
    elif Op == 2:
        #Segundo grafo
        grafo,dic_pesos = gera_grafo('cidades_alemanha59.txt')
        nome = 'cidades_alemanha59mst.png'
        arvore = Prim(grafo,dic_pesos)
        if Op2 == 1:
            nome = 'cidades_alemanha_'+str(numero_vertices)+'.png'
            if numero_vertices <= nx.number_of_edges(arvore):
                arvore = retira_aresta(arvore,dic_pesos,numero_vertices)
            else:
                print 'Número de vertices a serem retirados não compatível'
                exit(0)
        arvore_comunidades = nx.to_agraph(arvore)
        arvore_comunidades.layout('dot', args='-Nfontsize=10 -Nwidth=".2" -Nheight=".2" -Nmargin=0 -Gfontsize=8')
        arvore_comunidades.draw(nome)
        print 'arquivo criado com o nome: ',nome
    elif Op == 3:
        #Terceiro grafo
        grafo, dic_pesos = gera_grafo('cidades_EUA128.txt')
        nome = 'cidades_EUA128mst.png'
        arvore = Prim(grafo,dic_pesos)
        if Op2 == 1:
            nome = 'cidades_EUA_'+str(numero_vertices)+'.png'
            if numero_vertices <= nx.number_of_edges(arvore):
                arvore = retira_aresta(arvore,dic_pesos,numero_vertices)
            else:
                print 'Número de vertices a serem retirados não compatível'
                exit(0)
        arvore_comunidades = nx.to_agraph(arvore)
        arvore_comunidades.layout('dot', args='-Nfontsize=10 -Nwidth=".2" -Nheight=".2" -Nmargin=0 -Gfontsize=8')
        arvore_comunidades.draw(nome)
        print 'arquivo criado com o nome: ',nome
    else:
        print 'Número invalido'
        return

def gera_grafo(nome_arquivo):
    '''
    Parametro: nome_arquivo, tem nome do arquivo que possui a matriz de adjacencia
    Retorno: retorna o grafo correspondente à matriz de adjacencia
    Função: obter um grafo apartir da matriz de adjacencia
    '''
    #cria um grafo vazio
    g = nx.Graph() 
    #ler matriz de adjacencia
    matriz_adj = np.loadtxt(nome_arquivo)
    #Obter coordenadas em que o peso é diferente de zero
    linha, coluna = np.where(matriz_adj > 0)
    #Combina a linha com a coluna, formando as arestas.
    aresta = zip(linha,coluna)
    #Cria o dicionario com pesos
    dic_pesos = { (u, v) : matriz_adj[u][v] for u, v in aresta }
    #Preenche o grafo com as arestas e vertices    
    g.add_edges_from(aresta)
    #retorna o grafo
    return g, dic_pesos


def Prim(g,dic_pesos):
    '''
    Parametro: g, representando um grafo
    Retorno: arvore, arvore geradora minima
    Função: Retorna a MST (Minimun Spend Tree) ou arvore geradora minima
    do grafo recebido como parametro
    '''
    lista_prioridades = [(Inf,i) for i in range(int(nx.number_of_nodes(g)))]
    # lista_prioridades transformar em heap
    heapify(lista_prioridades) 
    # inserir nó 0 (assumindo que o nó 0 é a raiz) com prioridade 0
    push(lista_prioridades, (0, 0))
    #representação: posterior é o indice e anterior é o valor armazenado
    anteriores = [None for i in range(int(nx.number_of_nodes(g)))]
    # cria um dicionário que indica se um vertice v está no heap (se está no heap, ainda não foi processado)
    inheap = { v: True for v in g.nodes() }
    # cria um dicionário de pesos (evita a necessidade de utilizar a função verifica_vizinho)
    pesos = { v: float('inf') for v in g.nodes() }
    pesos[0] = 0;
 
    while lista_prioridades:
        no = pop(lista_prioridades)
        # testa se no ainda não foi removido do heap anteriormente (como não podemos atualizar os pesos, um nó pode repetir)
        if (inheap[no[1]]):
            inheap[no[1]] = False # foi retirado do heap pela primeira vez
        else:
            continue # já foi retirado do heap antes (repetido)

        #Seleciona cada vizinho
        for i in nx.neighbors(g,no[1]):
            #verifica se vizinho esta na lista de prioridades            
            if (inheap[i]): 
                #verifica se um no é anterior do outro   
                peso = dic_pesos[(no[1],i)]
                if peso < pesos[i]:
                    push(lista_prioridades, (peso, i))
                    anteriores[i] = no[1]
                    pesos[i] = peso
                    
    arestas = [(i,anteriores[i]) for i in range(len(anteriores))]
    arestas.pop(0) #Descarta o primeiro pois é a aresta da raiz, que não se liga com ninguém (0,None)
    g.clear()
    g.add_edges_from(arestas)
    return g
                       
def calcula_peso(g,dic_pesos):
    '''
    Parametros: g, grafo que se quer calcular o peso
                dic_pesos, peso de cada aresta
    Retorno: inteiro indicando a soma dos pesos das arestas
    Função: Calcular a soma dos pesos das arestas do grafo
    '''
    arestas = g.edges() #Retorna lista de arestas
    peso = 0
    #Conta o peso das arestas
    for i in arestas: peso += dic_pesos[i]
    return peso

def retira_aresta(g,peso,numero_retiradas):
    '''
    Parametros: g, arvore que representa a MST do grafo requerido
                peso, peso das arestas do grafo
                numero_retiradas, numero de arestas que serão retiradas
    Retorno: Grafo não conexo, formando comunidades, o número de comunidades
             se da por numero_retiradas+1
    Função: Remover as arestas de maior peso afim de formar comunidades
    '''
    
    while numero_retiradas:
        #Atribui em a e b os nós que formam uma aresta
        a,b = g.edges()[0]
        #Acha a aresta de maior peso no grafo
        for v in g.edges():
            if peso[v] > peso[(a,b)]:
                a, b = v
        #retira a aresta de maior peso
        g.remove_edge(a,b)
        numero_retiradas-=1
        
    return g        

if __name__ == "__main__":
    main()
