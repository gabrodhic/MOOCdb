class MoocData():
    def get_edges():
        raise NotImplementedError

    def anon_rows(self, rows):
        """
        rows ---> rows of edges list
        """

        mapping = {} #real id to "fake" id
        new_rows = []
        for r in rows:
            if r[0] not in mapping:
                mapping[r[0]] = random.randint(0,1000000)
            
            if r[1] not in mapping:
                mapping[r[1]] = random.randint(0,1000000)

            new_row = ( mapping[r[0]], mapping[r[1]], r[2] )
            new_rows.append(new_row)

        return new_rows, mapping

    def export_edges(self,f):
        rows = self.get_edges()
        rows, mapping = self.anon_rows(rows)

        with open(f+"_mapping", 'w') as out:
            out.write(json.dumps(mapping))
        
        with open(f+"_edges", 'w') as out:
            for r in rows:
                out.write( "%d,%d,%d\n" % (r[0], r[1], r[2]) )
