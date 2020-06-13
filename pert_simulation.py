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
        # Define los parametros de la distribucion triang para cada tarea.
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
    # TP1 TODO: Completar codigo
    # Esta funcion toma los 3 parametros de la distribucion triangular
    # y devuelve un numero psuedo-aleaotrio con esta distribucion.
    # Tenemos que adaptar estos parametros a lo que recibe la funcion
    # triang.ppf para aplicar el metodo de la transformada inversa. .

    # Primero un chequeo: si op == ps, entonces no hay mucho para simular.
    # Por que? Ya que no se puede generar numeros pseudo aleatorio que tenga el mismo valor para left y right. 
    if op == ps:
        return ml
    else:
        return numpy.random.triangular(op, ml, ps)       

    # Esta es la traduccion de parametros a realizar scipy.stats. Revisar la documentaicon
    # y entender como se representa la distribucion.
    #loc = op
    #scale = (ps - op)
    #c = (ml - loc)/scale

    # Si usan numpy.random, no son necesarias traducciones.

def simulate_tasks_duration(project_graph):
    # TP1 TODO: Completar codigo
    # Esta funcion el grafo con n tareas, cada cual con sus parametros de la 
    # correspondiente distribucion triangular, y devuelve una lista de 
    # n elementos, donde la posicion i corresponde a la duracion de la i-esima
    # tarea.
    # Sugerencia: recordar que la distribucion de la tarea i se encuentra en el 
    # diccionario project_graph.d[i]
    
    # Sacar el pass y reemplzar por el codigo
    ret = []
    for key, value in project_graph.get_tasks_dist_params().items():
        ret.append(simulate_triangular(value[0], value[1], value[2]))
    return ret

def get_path_duration(path, tasks_times):
    # TODO TP1: Completar codigo
    # Dado un camino, representado por path y la secuencia de tareas, y la
    # duracion de cada tarea (donde tasks_times[i] es la duracion de la i-esima
    # tarea, la funcion devuelve la duracion del camino dados esos tiempos.

    # Sacar el pass y reemplzar por el codigo
    duracion_camino = 0
    for i in path:
        duracion_camino += tasks_times[i]
    return duracion_camino
    

def get_project_duration(project_graph, tasks_times):
    # TODO TP1: Completar codigo
    # La duracion del proyecto corresponde al maximo de las duraciones de los caminos.
    # Recordatorio: los caminos se encuentran en project_graph.paths, y se pueden
    # obtener con el proyecto get_paths()

    # La funcion debe computar la duracion de cada uno de los caminos y retornar el maximo.

    # Sacar el pass y reemplzar por el codigo
    duraciones = []
    for path in project_graph.get_paths():
        duraciones.append(get_path_duration(path, tasks_times))
    return max(duraciones)
    

def simulate(n_sim,project_graph):
    # TODO TP1: Completar codigo
    # Esta funcion realiza n_sim simulaciones y analiza los resultados necesarios para el
    # arbol de decision.
    # Idealmente, puede devolver una lista con la duracion para cada una de las
    # simulaciones para su posterior analisis.

    # Sacar el pass y reemplzar por el codigo
    duracion_simulaciones = []
    for n in range(n_sim):
        duracion_simulaciones.append(get_project_duration(project_graph, simulate_tasks_duration(project_graph)))
    return duracion_simulaciones
        

def get_prob_in_range(vals, a, b):
    # TODO TP1: Completar codigo
    # Funcion auxiliar para analisis de resultados y calculo de probabilidades.
    # Dada una muestra de valores vals, calcula la proporcion de x in vals tales que 
    # a < x <= b.

    # Sacar el pass y reemplzar por el codigo
    in_range = [x for x in vals if a < x <= b]
    return len(in_range)/len(vals)

def main():
    # TODO TP1: Completar codigo

    # Fijamos la semilla, por reproducibilidad.
    numpy.random.seed(777) # Nos gusta el 7 :)
#    random.seed(777)

    # 300k por perder el deadline. Por ahora, 46.0
    # 150k por terminar en 40 o menos. Por ahora, mantenemos 40.0
    # Estos son los limites que nos importan.
    deadline = 47.0
    incentive = 40.0

    # Primer paso: consideramos el escenario sin contrataciones extra.
    graph_no_hire = ProjectGraph()
#    for key, value in graph_no_hire.get_tasks_dist_params().items():
#        print(simulate_triangular(value[0], value[1], value[2]))
        
#    print(graph_no_hire.get_tasks_dist_params())

    # TODO: simular en este contexto!
# =============================================================================
#     print(simulate_tasks_duration(graph_no_hire), end = "\n")
#     print(get_path_duration(graph_no_hire.get_paths()[0], simulate_tasks_duration(graph_no_hire)))
#     print(get_project_duration(graph_no_hire, simulate_tasks_duration(graph_no_hire)))
#     print(simulate(1000, graph_no_hire))
# =============================================================================
    simulacion_no_hire = simulate(1000, graph_no_hire)
    
    # Grafico de la distribucion de las simulaciones:
    plt.hist(simulacion_no_hire,density=True, color = "pink") 
    plt.xlabel("Sin contratación")
    
    plt.show()
    
    # TODO: Analizar los resultados.
    ganancia = 5000000
    inversion = -100000
    incentivo = 150000
    penalizacion = -300000
    
    prob_menor_igual_cuarenta_no_hire = get_prob_in_range(simulacion_no_hire, 0, incentive)
    prob_cuarenta_cuarentaysiete_no_hire = get_prob_in_range(simulacion_no_hire, incentive, deadline)
    prob_mas_cuarentaysiete_no_hire = get_prob_in_range(simulacion_no_hire, deadline, 100)
    
    print("Sin contratación:")
    print("Probabilidad  de terminar en la semana 40 o antes: ", prob_menor_igual_cuarenta_no_hire)
    print("Probabilidad  de terminar entre la semana 40 y 47: ", prob_cuarenta_cuarentaysiete_no_hire)
    print("Probabilidad  de terminar luego de la semana 47: ", prob_mas_cuarentaysiete_no_hire)
  
    # Tabla de pagos sin contrataciones:
    matriz_no_hire = [(ganancia + incentivo), (ganancia), (ganancia + penalizacion)]
        
    p_no_hire = [prob_menor_igual_cuarenta_no_hire,
                 prob_cuarenta_cuarentaysiete_no_hire,
                 prob_mas_cuarentaysiete_no_hire]
   
    print("Ganancia total:", numpy.dot(matriz_no_hire, p_no_hire))     
    print()

    # Segundo paso: analizar en el contexto que se hace la contratacion.
    # Esto lo representamos modificando la duracion de las tarea 2.
    graph_hire = graph_no_hire
    graph_hire.dist_params[2] = (6.0, 9.0, 13.0)

    # TODO: simular en este contexto!
    simulacion_hire = simulate(1000, graph_hire)
    
    # Grafico de la distribucion de las simulaciones:
    plt.hist(simulacion_hire,density=True, color = "grey")
    plt.xlabel("Con contratación")
    plt.show()
    
    # TODO: Analizar los resultados.
    # Tabla de pagos con contrataciones:
    prob_menor_igual_cuarenta_hire = get_prob_in_range(simulacion_hire, 0, incentive)
    prob_cuarenta_cuarentaysiete_hire = get_prob_in_range(simulacion_hire, incentive, deadline)
    prob_mas_cuarentaysiete_hire = get_prob_in_range(simulacion_hire, deadline, 100)
    
    print("Con contratación:")
    print("Probabilidad  de terminar en la semana 40 o antes: ", prob_menor_igual_cuarenta_hire)
    print("Probabilidad  de terminar entre la semana 40 y 47: ", prob_cuarenta_cuarentaysiete_hire)
    print("Probabilidad  de terminar luego de la semana 47: ", prob_mas_cuarentaysiete_hire)

    matriz_hire = [(ganancia + incentivo + inversion), (ganancia + inversion), (ganancia + penalizacion + inversion)]
        
    p_hire = [prob_menor_igual_cuarenta_hire,
              prob_cuarenta_cuarentaysiete_hire,
              prob_mas_cuarentaysiete_hire]
    
    print("Ganancia total:", numpy.dot(matriz_hire, p_hire))   
    print()

    # Resultado final: Decisión
    if numpy.dot(matriz_no_hire, p_no_hire) > numpy.dot(matriz_hire, p_hire):
        print("Alternativa elegida: No contratar")
    else:
        print("Alternativa elegida: Contratar")
        
if __name__ == "__main__":
    main()
