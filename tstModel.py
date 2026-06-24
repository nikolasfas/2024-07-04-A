from model.modello import Model

myModel = Model()
years = myModel.getAllYears()

myModel.buildGraph('disk', 2004)
nodes, edges = myModel.getGraphDetails()


bestPath, bestScore = myModel.handleCammino()
print(bestScore)
for node in bestPath:
    print(node)