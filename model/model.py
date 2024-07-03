from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.idMap = {}



    def buildGraph(self, anno, xg):
        nodi = DAO.getAllStates()
        self.grafo.add_nodes_from(nodi)
        for n in nodi:
            self.idMap[n.id] = n
        archi = DAO.getAllConnections(self.idMap)
        for c in archi:
            self.grafo.add_edge(c.state1, c.state2, weight=0)
        for n1 in self.grafo.nodes:
            for n2 in self.grafo.nodes:
                if self.grafo.has_edge(n1, n2):
                    peso = DAO.getPeso(n1.id, n2.id, anno, xg)
                    self.grafo[n1][n2]["weight"] = peso

    def getPesiAdiacenti(self):
        mappa = {}
        for n in self.grafo.nodes:
            peso = 0
            vicini = self.grafo.neighbors(n)
            for n1 in vicini:
                peso+=self.grafo[n][n1]["weight"]
            mappa[n.id] = peso
        return mappa
