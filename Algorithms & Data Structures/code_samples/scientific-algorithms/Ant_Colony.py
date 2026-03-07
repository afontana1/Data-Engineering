import networkx as nx
from random import randint as randi
import matplotlib.pyplot as plt


class Populate:
    G = nx.Graph()

    def __init__(self, n):
        self.N = n
        self.Crr = []
        self.randomPopulation()

    def randomPopulation(self):
        for i in range(self.N):
            for j in range(i + 1, self.N):
                z = randi(1, self.N * 10)
                self.Crr.append((i, j, z))

        print("Crr: ", self.Crr)
        self.ShowGraph(self.G, self.Crr)

    def ShowGraph(self, graph, crr):
        graph.add_weighted_edges_from(crr)
        pos = nx.shell_layout(graph)
        # pos = nx.kamada_kawai_layout(graph)
        # pos = nx.rescale_layout(graph)
        # pos = nx.spring_layout(graph)
        # pos = nx.spectral_layout(graph)
        # pos = nx.random_layout(graph)
        nx.draw_networkx_nodes(graph, pos, node_size=100)
        nx.draw_networkx_labels(graph, pos, font_size=13, font_family="sans-serif")
        labels = nx.get_edge_attributes(graph, "weight")
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, label_pos=0.38)

        nx.draw(graph, pos)
        plt.axis("off")
        plt.show()


# pop = Populate(6)


class Ant:
    def __init__(self, loc, n):
        self.Location = -1
        self.prevLocation = -1
        self.startState = loc
        self.N = n
        self.Visited = [False] * n
        self.setLocation(loc)

    def setLocation(self, loc):
        self.Location = loc
        self.Visited[loc] = True

    def updateLocation(self, loc):
        self.prevLocation = self.Location
        self.setLocation(loc)

    def GoStartState(self):
        # print("Array: ", self.Visited)
        print("loc: ", self.startState)
        self.Visited[self.startState] = False

    def reset(self, loc):
        self.Location = -1
        self.prevLocation = -1
        self.Visited = [False] * self.N
        self.setLocation(loc)


class AntColonyOptimization:
    Pheromone = 5.0
    EvapRate = 0.5
    Alpha = 1.2
    Beta = 0.8
    Iterations = 100

    def __init__(self, n):
        self.N = n
        self.Ants = []
        self.GraphEdges = []
        self.CityPheromone = []
        self.Initialize()

    def Initialize(self):
        pop = Populate(self.N)
        self.GraphEdges = pop.Crr
        self.EdgePheromone = [0.0] * len(self.GraphEdges)
        self.antPopulate()

    def antPopulate(self):
        for i in range(self.N):
            AntObject = Ant(i, self.N)
            self.Ants.append(AntObject)

    def getPathDistance(self, start, stop):
        for i in range(len(self.GraphEdges)):
            edge = self.GraphEdges[i]
            if edge[0] == start and edge[1] == stop:
                return (edge[2], i)
            elif edge[0] == stop and edge[1] == start:
                return (edge[2], i)

    def PheromoneIntensity(self, i, j, tempPeromone):
        print("edges: ", i, j)
        update = self.getPathDistance(i, j)
        distance = update[0]
        index = update[1]
        ph = AntColonyOptimization.Pheromone / distance
        tempPeromone[index] = [
            AntColonyOptimization.EvapRate * self.EdgePheromone[index] + ph,
            distance,
            index,
        ]

    def NextCity(self, inde):
        CurrentAnt = self.Ants[inde]
        MaxProbCity = -1
        MaxProbIndex = -1
        NormalizationValue = 0.0
        tempPheromone = [0.0] * len(self.GraphEdges)
        prob = [0] * len(self.GraphEdges)
        for i in range(self.N):
            if not CurrentAnt.Visited[i] and CurrentAnt.Location != i:
                self.PheromoneIntensity(CurrentAnt.Location, i, tempPheromone)

        # for i in range(len(tempPheromone)):
        #     print(tempPheromone[i])

        for i in range(len(tempPheromone)):
            if not tempPheromone[i] == 0.0:
                # print("tempPheromone[i][0]: ", i, tempPheromone[i][0])
                NormalizationValue += (
                    tempPheromone[i][0] ** AntColonyOptimization.Alpha
                ) * ((1.0 / tempPheromone[i][1]) ** AntColonyOptimization.Beta)
        for i in range(len(self.GraphEdges)):
            if not tempPheromone[i] == 0.0 and tempPheromone[i][0] != 0.0:
                # print("temp: ", tempPheromone[i])
                prob[i] = (
                    (tempPheromone[i][0] ** AntColonyOptimization.Alpha)
                    * ((1.0 / tempPheromone[i][1]) ** AntColonyOptimization.Beta)
                ) / NormalizationValue
                if prob[i] >= MaxProbCity:
                    MaxProbCity = prob[i]
                    MaxProbIndex = i
        print(tempPheromone[MaxProbIndex])
        index = tempPheromone[MaxProbIndex][2]
        print("index: ", index, self.Ants[inde].Location, self.GraphEdges[index][1])
        CurrentAnt.updateLocation(self.GraphEdges[index][1])
        print("return: ", (tempPheromone[MaxProbIndex], index))
        return (tempPheromone[MaxProbIndex], index)

    def updatePheromone(self, pheromone):
        for i in range(self.N):
            # print(pheromone[i])
            index = pheromone[i][1]
            self.EdgePheromone[index] = pheromone[i][0][0]

    def Reset(self):
        for i in range(self.N):
            self.Ants[i].reset(i)

    def ShowSolution(self):
        newGraph = []
        for i in range(len(self.GraphEdges)):
            newGraph.append(
                (
                    self.GraphEdges[i][0],
                    self.GraphEdges[i][1],
                    self.EdgePheromone[i] * 100,
                )
            )
        # print("newGraph: ", newGraph)
        Populate.ShowGraph(self, nx.Graph(), newGraph)

    def StartState(self, index):
        CurrentAnt = self.Ants[index]
        print(CurrentAnt.Location, CurrentAnt.startState)
        update = self.getPathDistance(CurrentAnt.Location, CurrentAnt.startState)
        distance = update[0]
        index = update[1]
        ph = AntColonyOptimization.Pheromone / distance
        tempPeromone = [
            AntColonyOptimization.EvapRate * self.EdgePheromone[index] + ph,
            distance,
            index,
        ]
        self.EdgePheromone[index] = tempPeromone[0]

    def GoBackToStart(self):
        Pheromone = [0] * self.N
        for j in range(self.N):
            if j != self.Ants[j].Location:
                self.Ants[j].GoStartState()
                Pheromone[j] = self.StartState(j)

    def run(self):
        for i in range(AntColonyOptimization.Iterations):
            for k in range(self.N):
                Pheromone = [0] * self.N
                for j in range(self.N):
                    Pheromone[j] = self.NextCity(j)
                self.updatePheromone(Pheromone)
            self.GoBackToStart()
            self.Reset()

        self.ShowSolution()


if __name__ == "__main__":
    aco = AntColonyOptimization(5)
    aco.run()
