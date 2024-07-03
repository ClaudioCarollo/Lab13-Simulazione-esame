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
        self.grafo = nx.Graph()

    def getAllYears(self):
        anni = DAO.getAllYears()
        return anni

    def getAllShapes(self, year):
        forme = DAO.getAllShapes(year)
        return forme

    def buildGraph(self, shape, year):
        nodi = DAO.getAllStates()
        self.grafo.add_nodes_from(nodi)
        for n in self.grafo.nodes:
            self.idMap[n.id] = n
        connessioni = DAO.getAllConnessioni(self.idMap)
        for c in connessioni:
            self.grafo.add_edge(c.stato1, c.stato2, weight = 0)
        for n1 in self.grafo.nodes:
            for n2 in self.grafo.nodes:
                if self.grafo.has_edge(n1, n2):
                    peso = DAO.getAllPesi(n1.id, n2.id, shape, year)
                    self.grafo[n1][n2]["weight"] = peso

    def getPath(self):
        # caching con variabili della classe (percorso migliore e peso maggiore)
        self._bestComp = []
        self._bestdTot = 0
        # inizializzo il parziale con il nodo iniziale
        parziale = []

        for a in self.grafo.nodes:
            if a not in parziale:
                parziale.append(a)
                self._ricorsionev2(parziale)
                parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking
        return self._bestComp, self._bestdTot

    def _ricorsionev2(self, parziale):
        # verifico se soluzione è migliore di quella salvata in cache

        if self.getScore(parziale) > self._bestdTot:
            # se lo è aggiorno i valori migliori
            self._bestComp = copy.deepcopy(parziale)
            self._bestdTot = self.getScore(parziale)
        # verifico se posso aggiungere un altro elemento
        comp = self.grafo.neighbors(parziale[-1])
        for a in comp:
            if a not in parziale:
                if len(parziale)<2:
                    parziale.append(a)
                    self._ricorsionev2(parziale)
                    parziale.pop()
                elif self.grafo[parziale[-1]][a]["weight"] > self.grafo[parziale[-2]][parziale[-1]]["weight"]:
                    parziale.append(a)
                    self._ricorsionev2(parziale)
                    parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking


    def getScore(self, list):
        score = 0
        for i in range(0, len(list)-1):
            score += distance.geodesic((list[i].Lat, list[i].Lng), (list[i+1].Lat, list[i+1].Lng)).km
        return score
