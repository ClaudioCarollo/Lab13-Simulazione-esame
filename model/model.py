from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.idMap = {}

    def getShapes(self, year):
        forme = DAO.getShapes(year)
        return forme

    def buildGraph(self, shape, year):
        nodi = DAO.getAllStates()
        self.grafo.add_nodes_from(nodi)
        for n in self.grafo.nodes:
            self.idMap[n.id] = n
        vicini = DAO.getAllEdges(self.idMap)
        for v in vicini:
            self.grafo.add_edge(v.stato1, v.stato2)
        for n1 in self.grafo.nodes:
            for n2 in self.grafo.nodes:
                if self.grafo.has_edge(n1, n2):
                    peso = DAO.getPeso(shape, year, n1.id, n2.id)
                    self.grafo[n1][n2]["weight"] = peso




