#Dulce Ambrosio - 231143
#03 de marzo del 2024
#Hoja 5 de ADT

#Importar las librerias
import simpy
import numpy as np
import math

#semilla
np.random.seed(100)
#Lista para los promedios
tiempos_promedios=[] 

#Clase para el proceso
class Proceso:

    #Función para inicializar las variables para el proceso
    def __init__(self, name, env, ram, cpu):
        self.name = name
        self.instrucciones = np.random.randint(1,11)
        self.memoria = np.random.randint(1,11)
        self.hora_inicio = 0
        self.hora_fin = 0
        self.totalTiempo = 0

    #Funcion para iniciar el proceso 
    def run(self):
        #se cloca que el valor de la hora de inicio empieza en el entorno
        self.hora_inicio = env.now
        print(f"{env.now} Inicia proceso {self.name}.")
        
        # Solicitar memoria
        with ram.get(self.memoria) as req:
            yield req
            print(f"{env.now} {self.name} solicita {self.memoria} de RAM.")

            # Solicitar CPU
            with cpu.request() as req2:
                yield req2
                print(f"{env.now} {self.name} solicita CPU.")

                # Ejecutar instrucciones
                while self.instrucciones > 0:
                    yield env.timeout(1)  
                    self.instrucciones -= 3
                    if self.instrucciones <= 0:
                        self.instrucciones = 0
                    else:
                        self.instrucciones = self.instrucciones
                    print(f"{env.now} {self.name} ejecutando instrucción. Instrucciones restantes: {self.instrucciones}")

                    # Simular interrupciones (I/O)
                    if np.random.random() < 0.1:  
                        print(f"{env.now} {self.name} pasa a operaciones de I/O.")
                        yield env.timeout(np.random.randint(1, 6))  
                self.hora_fin = env.now

                print(f"{env.now} {self.name} termina de ejecutar instrucciones.")
            ram.put(self.memoria) #devolver la memoria ram al cpu
            self.hora_fin = env.now #se coloca que la hora de fin es del entorno
            self.totalTiempo = int(self.hora_fin-self.hora_inicio) #se calcula el tiempo total
            tiempos_promedios.append(self.totalTiempo) #se ingresan los tiempos a la lista

# Función para crear procesos
def crear_procesos(env, ram, cpu, max_num=25, freq=1):
    for i in range(max_num):
        proceso = Proceso(f"Proceso-{i+1}", env, ram, cpu)
        env.process(proceso.run())
        yield env.timeout(freq)

#Función para el promedio
def promedio(s): return sum(s) * 1.0 / len(s)

# Crear entorno de simulación
env = simpy.Environment()

# Definir recursos (RAM y CPU)
ram = simpy.Container(env, capacity=100, init=100)
cpu = simpy.Resource(env, capacity=2)

# Crear procesos 
env.process(crear_procesos(env, ram, cpu))

# Ejecutar simulación
env.run()

# Calcular promedio de tiempos totales y desviación estándar
tiempo_promedio_total = promedio(tiempos_promedios)
varianza = sum((x - tiempo_promedio_total) ** 2 for x in tiempos_promedios) / len(tiempos_promedios)
desviacion_estandar = math.sqrt(varianza)

#se imprime el tiempo promedio y la desviación
print("El promedio del tiempo es:", tiempo_promedio_total)
print("La desviación estándar es:", desviacion_estandar)
