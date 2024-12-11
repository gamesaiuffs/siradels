import psycopg2

class Conexao(object):
    _db=None
    def __init__(self):
        self._db = psycopg2.connect(host='localhost', database='ia', user='postgres', password='admin')
    
    def executar(self, sql):
        try:
            cur=self._db.cursor()
            cur.execute(sql)
            cur.close()
            self._db.commit()
        except:
            return False
        return True
    
    def consultar(self, sql):
        rs=None
        try:
            cur=self._db.cursor()
            cur.execute(sql)
            rs=cur.fetchall()
        except:
            return None
        return rs
    
    def fechar(self):
        self._db.close()    
        