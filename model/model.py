import copy

import geopy

from database.DAO import DAO
import networkx as nx
from geopy import distance

class Model:
    def __init__(self):
        self._bestComp = None
        self._bestdTot = None
        self.idMap = {}
        self.grafo = nx.DiGraph()

    def getAllYears(self):
        mappa = {}
        anni = DAO.getAllYears()
        for a in anni:
            mappa[a] = DAO.getAllNumber(a)
        return mappa


    def buildGraph(self, year):
        self.grafo.clear()
        nodi = DAO.getAllNodes(year)
        self.grafo.add_nodes_from(nodi)
        stati = DAO.getAllStates()
        for n in stati:
            self.idMap[n.id.lower()] = n
        connessioni = DAO.getAllConnessioni(self.idMap, year)
        for c in connessioni:
            self.grafo.add_edge(c.stato1, c.stato2)


    def getComponenteConnessa(self, nodo):
        componente = nx.bfs_tree(self.grafo, nodo)
        return componente

    def getPath(self, n):
        # caching con variabili della classe (percorso migliore e peso maggiore)
        self._bestComp = []
        self._bestdTot = 0
        # inizializzo il parziale con il nodo iniziale
        parziale = [n]
        successori = self.grafo.successors(n)
        for a in successori:
            if a not in parziale:
                parziale.append(a)
                self._ricorsionev2(parziale)
                parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking
        return self._bestComp

    def _ricorsionev2(self, parziale):
        # verifico se soluzione è migliore di quella salvata in cache

        if len(parziale) > self._bestdTot:
            # se lo è aggiorno i valori migliori
            self._bestComp = copy.deepcopy(parziale)
            self._bestdTot = len(parziale)
            return
        # verifico se posso aggiungere un altro elemento
        successori = self.grafo.successors(parziale[-1])
        for a in successori:
            if a not in parziale:
                parziale.append(a)
                self._ricorsionev2(parziale)
                parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking

