import numpy
import math
import random
import statistics
import matplotlib.pyplot as plt
from scipy.stats import expon,uniform,triang
import sys

class ProjectGraph:
    def __init__(self):
        self.n = 14
        self.m = 6
        self.paths = self._load_paths()
        self.dist_params = self._load_tasks_dist_params()

    def get_paths(self):
        return self.paths

    def get_n_tasks(self):
        return self.n

    def get_tasks_dist_params(self):
        return self.dist_params

    def _load_tasks_dist_params(self):
        # Define los parametros de la distribucion triangular para cada tarea.
        # Notar que es estatico, pero podria ser dinamico (tomarse de alguna
        # otra fuente). Usa un diccionario.
        d = {}
        d[0] = (1.0, 2.0, 3.0)
        d[1] = (2.0, 3.5, 8.0)
        d[2] = (6.0, 9.0, 18.0)
        d[3] = (4.0, 5.5, 10.0)
        d[4] = (1.0, 4.5, 5.0)
        d[5] = (4.0, 4.0, 10.0)
        d[6] = (5.0, 6.5, 11.0)
        d[7] = (5.0, 8.0, 17.0)
        d[8] = (3.0, 7.5, 9.0)
        d[9] = (3.0, 9.0, 9.0)
        d[10] = (4.0, 4.0, 4.0)
        d[11] = (1.0, 5.5, 7.0)
        d[12] = (1.0, 2.0, 3.0)
        d[13] = (5.0, 5.5, 9.0)
        return d

    def _load_paths(self):
        # Define los caminos. 
        # Notar que es estatico. Podria ser conveniente tener otra
        # representacion e, incluso, otra estructura para el grafo general.
        return [[0,1,2,3,6,7,12],[0,1,2,4,7,12],[0,1,2,4,5,9,10,13],[0,1,2,4,5,9,11,13],[0,1,2,8,9,10,13],[0,1,2,8,9,11,13]]
    

def simulate_triangular(op,ml,ps):
    # Esta funcion toma los 3 parametros de la distribucion triangular
    # y devuelve un numero psuedo-aleaotrio con esta distribucion.
    
    if op == ps: # Tenemos en cuenta que si op == ps, no debemos simular nada ya que el valor es el mismo para todos los escenarios.
        return ml
    else:
        return numpy.random.triangular(op, ml, ps)       

def simulate_tasks_duration(project_graph):
    # Esta funcion el grafo con n tareas, cada cual con sus parametros de la 
    # correspondiente distribucion triangular, y devuelve una lista de 
    # n elementos, donde la posicion i corresponde a la duracion de la i-esima
    # tarea.
    ret = [] # Creamos una lista vacia. 
    for key, value in project_graph.get_tasks_dist_params().items(): # Para cada key-value en el diccionario con las estimaciones de duracion de cada tarea...
        ret.append(simulate_triangular(value[0], value[1], value[2])) # Agrega a la lista el numero aleatorio con dist. triangular que corresponde a cada tarea, 
                                                                      # teniendo en cuenta las estimaciones de duracion.
    return ret # Devolve la lista con los numeros aleatorios que corresponden a la duracion calculada con la dist. triangular de cada tarea.

def get_path_duration(path, tasks_times):
    # Dado un camino, representado por path y la secuencia de tareas, y la
    # duracion de cada tarea (donde tasks_times[i] es la duracion de la i-esima
    # tarea), la funcion devuelve la duracion del camino dados esos tiempos.

    duracion_camino = 0 # Inicializamos una variable en 0.
    for i in path: # Para cada tarea en el camino que se le pasa como arguemento...
        duracion_camino += tasks_times[i] # Suma en duracion_camino el tiempo que requiere cada tarea dentro del camino.
    return duracion_camino # Devolve el tiempo total del camino.
    

def get_project_duration(project_graph, tasks_times):
    # La duracion del proyecto corresponde al maximo de las duraciones de los caminos.
    # La funcion computa la duracion de cada uno de los caminos y retornar el maximo.

    duraciones = [] # Creamos una lista vacia.
    for path in project_graph.get_paths(): # Para cada camino en la lista de los 6 caminos determinada en el tipo ProjectGraph...
        duraciones.append(get_path_duration(path, tasks_times)) # Agrega a la lista la duración del camino utilizando la función get_path_duration.
    return max(duraciones) # Retorna el maximo en duraciones, es decir, el camino que mas tiempo requiere.
    

def simulate(n_sim,project_graph):
    # Esta funcion realiza n_sim simulaciones y analiza los resultados necesarios para el
    # arbol de decision.
    # Devuelve una lista con la duracion para cada una de las simulaciones para su posterior analisis.

    duracion_simulaciones = [] # Creamos una lista vacia. 
    for n in range(n_sim): # Para n en el rango de cantidad de simulaciones que se pasa como arguemento...
        duracion_simulaciones.append(get_project_duration(project_graph, simulate_tasks_duration(project_graph)))
        # Agrega a la lista el tiempo que tarda cada proyecto utilizando la funcion get_project_duration. 
    return duracion_simulaciones # Devolve la lista con las n_sim simulaciones correspondientes a la duracion de cada proyecto.
        

def get_prob_in_range(vals, a, b):
    # Funcion auxiliar para analisis de resultados y calculo de probabilidades.
    # Dada una muestra de valores vals, calculamos la proporcion de x in vals tales que 
    # a < x <= b.

    in_range = [x for x in vals if a < x <= b] # Agrega a la lista a x para x en vals si x esta en el rango (a,b]
    return len(in_range)/len(vals)

def main():
    # Fijamos la semilla, por reproducibilidad.
    numpy.random.seed(777) # Nos gusta el 7 :)

    # Definimos:
    # Limites:
    deadline = 47.0
    incentive = 40.0
    
    # Posibles resultados:
    ganancia = 5000000
    inversion = -100000
    incentivo = 150000
    penalizacion = -300000

    # Primer paso: consideramos el escenario sin contrataciones extra.
    graph_no_hire = ProjectGraph() 

    simulacion_no_hire = simulate(1000, graph_no_hire) # Definimos las 1.000 simulaciones cuando no hay contrataciones extra.
    
    # Grafico de la distribucion de las simulaciones:
    plt.hist(simulacion_no_hire,density=True, color = "pink") 
    plt.xlabel("Sin contratación")    
    plt.show()
    
    # Analizamos los resultados:
    prob_menor_igual_cuarenta_no_hire = get_prob_in_range(simulacion_no_hire, 0, incentive) # Probabilidad de terminar en 40 semanas o menos.
    prob_cuarenta_cuarentaysiete_no_hire = get_prob_in_range(simulacion_no_hire, incentive, deadline) # Probabilidad de terminar entre la semana 40 y 47.
    prob_mas_cuarentaysiete_no_hire = get_prob_in_range(simulacion_no_hire, deadline, 100) # Probabilidad de terminar despues de la semana 47.
    
    # Imprimimos por pantalla los resultados:
    print("Sin contratación:")
    print("Probabilidad  de terminar en la semana 40 o antes: ", prob_menor_igual_cuarenta_no_hire)
    print("Probabilidad  de terminar entre la semana 40 y 47: ", prob_cuarenta_cuarentaysiete_no_hire)
    print("Probabilidad  de terminar luego de la semana 47: ", prob_mas_cuarentaysiete_no_hire)
  
    # Tabla de pagos sin contrataciones:
    matriz_no_hire = [(ganancia + incentivo), (ganancia), (ganancia + penalizacion)]
    
    # Tabla de probabilidades:    
    p_no_hire = [prob_menor_igual_cuarenta_no_hire,
                 prob_cuarenta_cuarentaysiete_no_hire,
                 prob_mas_cuarentaysiete_no_hire]
    
    # Imprimimos por pantalla la ganancia total sin contratacion:
    print("Ganancia total:", numpy.dot(matriz_no_hire, p_no_hire)) # Hacemos sumaproducto entre las matrices.
    print()

    # Segundo paso: consideramos el escenario con contratacion extra.
    # Esto lo representamos modificando la duracion de las tarea 2.
    graph_hire = graph_no_hire
    graph_hire.dist_params[2] = (6.0, 9.0, 13.0)
    
    simulacion_hire = simulate(1000, graph_hire) # Definimos las 1.000 simulaciones cuando hay contrataciones extra.
    
    # Grafico de la distribucion de las simulaciones:
    plt.hist(simulacion_hire,density=True, color = "grey")
    plt.xlabel("Con contratación")
    plt.show()
    
    # Grafico con las dist. de cuando hay contratacion extra y cuando no:
    plt.hist(simulacion_no_hire,density=True, color = "pink") 
    plt.hist(simulacion_hire,density=True, color = "grey")
    plt.show()
    
    # Analizamos los resultados.
    prob_menor_igual_cuarenta_hire = get_prob_in_range(simulacion_hire, 0, incentive) # Probabilidad de terminar en 40 semanas o menos.
    prob_cuarenta_cuarentaysiete_hire = get_prob_in_range(simulacion_hire, incentive, deadline) # Probabilidad de terminar entre la semana 40 y 47.
    prob_mas_cuarentaysiete_hire = get_prob_in_range(simulacion_hire, deadline, 100) # Probabilidad de terminar despues de la semana 47.
    
    # Imprimimos por pantalla los resultados:
    print("Con contratación:")
    print("Probabilidad  de terminar en la semana 40 o antes: ", prob_menor_igual_cuarenta_hire)
    print("Probabilidad  de terminar entre la semana 40 y 47: ", prob_cuarenta_cuarentaysiete_hire)
    print("Probabilidad  de terminar luego de la semana 47: ", prob_mas_cuarentaysiete_hire)
    
    # Tabla de pagos con contrataciones:
    matriz_hire = [(ganancia + incentivo + inversion), (ganancia + inversion), (ganancia + penalizacion + inversion)]
    
    # Tabla de probabilidades:    
    p_hire = [prob_menor_igual_cuarenta_hire,
              prob_cuarenta_cuarentaysiete_hire,
              prob_mas_cuarentaysiete_hire]
    
    # Imprimimos por pantalla la ganancia total con contratacion:
    print("Ganancia total:", numpy.dot(matriz_hire, p_hire)) # Hacemos sumaproducto entre las matrices.
    print()

    # Resultado final: Decisión
    if numpy.dot(matriz_no_hire, p_no_hire) > numpy.dot(matriz_hire, p_hire):
        print("Alternativa elegida: No contratar")
    else:
        print("Alternativa elegida: Contratar")
        
if __name__ == "__main__":
    main()
