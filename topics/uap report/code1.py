class MockMOOC(MoocData):
    """
    Mock datasource. Takes a file name. look at mock_data.csv for example
    """
    def __init__(self, f):
        self.f = f

    def get_edges(self):
        edges = []
        with open(self.f, "r") as edges:
            edges = [e.split(",") for e in edges]
            return [(int(e[0]), int(e[1]), int(e[2])) for e in edges]