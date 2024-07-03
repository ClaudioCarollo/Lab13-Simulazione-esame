from database.DB_connect import DBConnect
from model.neighbors import Neighbor
from model.state import State


class DAO():
    @staticmethod
    def getAllStates():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct * 
                            from state s"""
            cursor.execute(query)
            for row in cursor:
                result.append(State(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllConnections(idmap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select n.state1 as stato1, n.state2 as stato2 
                        from neighbor n
                        where n.state1 < n.state2 """
            cursor.execute(query)
            for row in cursor:
                result.append(Neighbor(idmap[row["stato1"]], idmap[row["stato2"]]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getPeso(s1, s2, anno, xg):
        cnx = DBConnect.get_connection()
        result = 0
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ SELECT (count(distinct s1.id)+ count(distinct s2.id)) as peso 
                        FROM 
                            neighbor n, sighting s1, sighting s2
                        WHERE 
                            n.state1 = s1.state
                            and n.state2 = s2.state
                            and YEAR(s1.datetime) = %s
                            AND YEAR(s2.datetime) = %s
                            AND ABS(DATEDIFF(s1.datetime, s2.datetime)) <= %s
                            and s1.state in (%s, %s)
                            and s2.state in (%s, %s)
                            and s1.state< s2.state"""
            cursor.execute(query, (anno, anno, xg, s1, s2, s2, s1))
            for row in cursor:
                result = row["peso"]
            cursor.close()
            cnx.close()
        return result
