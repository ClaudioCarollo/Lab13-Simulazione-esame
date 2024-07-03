from database.DB_connect import DBConnect
from model.connessione import Neighbor
from model.state import State


class DAO():
    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(s.`datetime`) as year
                        from sighting s"""
            cursor.execute(query, )
            for row in cursor:
                result.append(row["year"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllShapes(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.shape as shape
                        from sighting s 
                        where year(s.`datetime`) = %s
                        order by s.shape """
            cursor.execute(query, (year, ))
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
    def getAllConnessioni(idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT n.state1 AS s1, n.state2 AS s2
                           FROM neighbor n
                           WHERE n.state1 < n.state2"""
        cursor.execute(query)
        for row in cursor:
            result.append(Neighbor(idMap[row["s1"]], idMap[row["s2"]]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllPesi(s1, s2, shape, year):
        conn = DBConnect.get_connection()
        result = 0
        cursor = conn.cursor(dictionary=True)
        query = """SELECT COUNT(*) AS peso
                           FROM sighting s1
                           WHERE s1.state IN (%s, %s) AND s1.shape = %s AND YEAR(s1.datetime) = %s"""
        cursor.execute(query, (s1, s2, shape, year))
        for row in cursor:
            result = row["peso"]
        cursor.close()
        conn.close()
        return result




