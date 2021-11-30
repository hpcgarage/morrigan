import sst
#import networkx as nx
#import matplotlib
#import matplotlib.pyplot as plt
#matplotlib.use("Agg")

component_count = {}
#build = False
#graph = nx.Graph()

#def build_graph():
#    build = True

#def get_graph(filename='graph.png'):
#    f = plt.figure()
#    nx.draw(graph, ax=f.add_subplot(111))
#    f.savefig(filename)

#def anon(component):
#    if component in component_count:
#        num = component_count[component]
#        component_count[component] = num + 1
#    else:
#        num = 0
#        component_count[component] = 1
#
#    name = "anon_" + component + "_" + str(num)
#    return sst.Component(name, component)

def mk(comp, params):
      comp.addParams(params)
      return comp

def mklink(e1, e2):
      link = sst.Link("link_" + e1[0].getFullName() + "[" + e1[1] + "]" + "_" +
                                e2[0].getFullName() + "[" + e2[1] + "]" )
      #print("link_" + e1[0].getFullName() + "[" + e1[1] + "]" + "_" +
      #                          e2[0].getFullName() + "[" + e2[1] + "]")
      link.connect(e1, e2)

#      if (build):
#        graph.add_edge(e1[0].getFullName(), e2[0].getFullName())

      return link

