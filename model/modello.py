import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()

    def handleCammino(self):

        self._bestPath = []
        self._bestScore = 0
        parziale = []

        for node in self._graph.nodes:
            month = node.datetime.month
            duration = node.duration
            sameMonth = {
                month: 1
            }
            parziale.append(node)
            self._ricorsione(parziale, duration, month, 100, sameMonth)
            parziale.pop()

        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, duration, oldMonth, currentScore, sameMonth):

        if currentScore > self._bestScore:
            self._bestScore = currentScore
            self._bestPath = copy.deepcopy(parziale)

        for node in self._graph.successors(parziale[-1]):

            newDuration = node.duration
            if newDuration > duration and node not in parziale:

                 newMonth = node.datetime.month

                 if sameMonth.get(newMonth, 0) < 3:

                     if  newMonth == oldMonth:
                         newScore = currentScore + 300

                     else:
                         newScore = currentScore + 100

                     sameMonth[newMonth] = sameMonth.get(newMonth, 0) + 1
                     parziale.append(node)

                     self._ricorsione(parziale, newDuration, newMonth, newScore, sameMonth)

                     parziale.pop()
                     sameMonth[newMonth] -= 1

                     if sameMonth[newMonth] == 0:
                         del sameMonth[newMonth]





    def getComponentsGraph(self):
        connComp = nx.weakly_connected_components(self._graph)
        maxConnComp = max(connComp, key=len)
        lenConnComp = len(maxConnComp)
        return lenConnComp, maxConnComp

    def buildGraph(self, shape, year):

        rightSightings = DAO.get_filter_sightings(shape, year)
        self._graph.add_nodes_from(rightSightings)

        for n1 in self._graph.nodes:
            for n2 in self._graph.nodes:

                if n1 != n2:
                    if n1.state == n2.state:

                        date1 = n1.datetime
                        date2 = n2.datetime

                        if date1 < date2:
                            self._graph.add_edge(n1, n2)
                        elif date1 > date2:
                            self._graph.add_edge(n2, n1)

    def getGraphDetails(self):
        nodes = self._graph.nodes
        edges = self._graph.edges
        return nodes, edges


    def getAllYears(self):
        sightings = DAO.get_all_sightings()
        yearsSet = set()
        for sighting in sightings:
            year = sighting.datetime.year
            yearsSet.add(year)
        yearsList = [int(year) for year in yearsSet]
        yearsList.sort(reverse=True)
        return yearsList

    def getAllShapes(self):
        sightings = DAO.get_all_sightings()
        shapesSet = set()
        for sighting in sightings:
            shape = sighting.shape
            if shape != "":
                shapesSet.add(shape)
        shapeList = [shape for shape in shapesSet]
        shapeList.sort()
        return shapeList