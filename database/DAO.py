from database.DB_connect import DBConnect
from model.neighbors import Neighbors
from model.state import State


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getShapes(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.shape as shape
                        from sighting s
                        where year(s.`datetime`) = %s
                        order by s.shape"""
            cursor.execute(query, (year,))
            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllStates():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                        from state s"""
            cursor.execute(query)
            for row in cursor:
                result.append(State(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllEdges(idmap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select n.state1 as stato1, n.state2 as stato2
                        from neighbor n"""
            cursor.execute(query)
            for row in cursor:
                result.append(Neighbors(idmap[row["stato1"]], idmap[row["stato2"]]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getPeso(shape, year, state1, state2):
        cnx = DBConnect.get_connection()
        result = 0
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select  count(*) as peso
                        from neighbor n, sighting s1, sighting s2 
                        where n.state1 = upper(s1.state)
                        and n.state2 = upper(s2.state) 
                        and s1.shape = s2.shape
                        and year(s2.`datetime`) = year(s1.`datetime`) 
                        and s1.shape = %s
                        and year(s1.`datetime`) = %s
                        and n.state1 = %s
                        and n.state2 = %s """
            cursor.execute(query, (shape, year, state1, state2))
            for row in cursor:
                result = row["peso"]
            cursor.close()
            cnx.close()
        return result

