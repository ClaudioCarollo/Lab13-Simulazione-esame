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
    def getAllNumber(year):
        cnx = DBConnect.get_connection()
        result = 0
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select count(*) as numero
from sighting s 
where s.country ='us' and year(s.`datetime`) = %s  """
            cursor.execute(query, (year, ))
            for row in cursor:
                result = row["numero"]
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s2.id as id, s2.Name as Name, s2.Capital as Capital, s2.Lat as Lat, s2.Lng as Lng, s2.Area as Area, s2.Population as Population, s2.Neighbors as Neighbors
from sighting s, state s2 
where s.state = s2.id and year (s.`datetime`) = %s
order by s2.id """
            cursor.execute(query, (anno,))
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
    def getAllConnessioni(idMap, year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct s1.state as state1, s2.state as state2
from sighting s1, sighting s2
where year(s2.`datetime`) = %s and year(s1.`datetime`) = %s and s1.`datetime`<s2.`datetime` and s1.state != s2.state
group by s1.state, s2.state"""
        cursor.execute(query, (year, year))
        for row in cursor:
            result.append(Neighbor(idMap[row["state1"]], idMap[row["state2"]]))
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




