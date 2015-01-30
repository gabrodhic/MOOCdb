class MySQLMOOC(MoocData):
    def __init__(self, db=None, mock=True):
        mysql = db
        self.cur = mysql.cursor()
    
    def get_edges(self, start_date='2012-03-04 16:57:49', end_date='2012-03-06 16:57:49'):
        query = """
        SELECT child.user_id, parent.user_id,  count(*)
        FROM moocdb.collaborations  child
        JOIN moocdb.collaborations parent
        ON parent.collaboration_id=child.collaboration_parent_id
        WHERE child.collaboration_timestamp BETWEEN %s and %s
        GROUP BY child.user_id, parent.user_id;
        """ 
        
        self.cur.execute(query, (start_date, end_date))
        rows = self.cur.fetchall()
            
        return rows