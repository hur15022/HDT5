##Algoritmos y Estructura de datos
##Hoja de Trabajo 5
##Juan Pablo Zea 15401
##Diego Hurtarte 15022


import simpy
import random
import math

seed=10
procesos=200
cant=10.0

global tiempoP
tiempoP=1
global tiempoIO
tiempoIO=5
global tiempoTotal
tiempoTotal=0
global instrucciones
instrucciones=10
global memoria
memoria=10
global instruct

##Funcion que crea los procesos y los envia para ser ejecutados
def fuente(env,cpu,i_o,ram,new,intervalo):
    global instrucciones
    global memoria
    for i in range(new):
        j=i+1
        instruc=random.randint(1,instrucciones)
        mem=random.randint(1,memoria)
        proc=proceso(env,'%s' % j,cpu,ram,i_o,mem,instruc)
        env.process(proc)
        t=random.expovariate(1.0/intervalo)
        yield env.timeout(t)

##funcion que crea el procesos y lo ejecuta     
def proceso(env,nombre,cpu,ram,i_o,memoria,instrucciones):
    global tiempoTotal
    global tiempoP
    global instruct
    ##se crea un nuevo proceso
    crear=env.now
    print ('se crea el proceso %s en el tiempo %s' % (nombre,crear))
    with ram.get(memoria) as req:
        yield req
        listo=env.now
        ##el proceso se pasa al estado ready
        print('el proceso %s paso a estar listo en el tiempo %s' % (nombre,listo))
        ##se pasa el proceso para ejecutar, hasta que termine
        while (instrucciones>0):
            with cpu.request() as req1:
                yield req1
                p=env.now
                print('se empezo el proceso %s en el tiempo %s'%(nombre,p))
                yield env.timeout(tiempoP)
                p=env.now
                ##se termina de procesar
                print ('se ha procesado %s en el tiempo %s'%(nombre,p))
                i=instrucciones-instruct

                ##Si el proceso se queda sin insturcciones se termina, si no este puede pasar al estado I/O
                if i<0:
                    terminar=env.now
                    tp=terminar-crear
                    tiempoTotal=tiempoTotal+tp
                    ##se acaban las isntrucciones de un proceso y se termina
                    print ('se termino de ejecutar el proceso %s en el tiempo %s'% (nombre,terminar))
                    instrucciones=0  
                else:
                    ##se genera un numero random y se evalua, si es 0 entra al proceso I/O
                    instrucciones=instrucciones-instruct
                    m=random.randint(0,1)
                    if m==0:
                        with i_o.request() as req2:
                            yield req2
                            tiemp=env.now
                            print ('se paso el proceso %s al estado I/O en el tiempo %s'%(nombre,tiemp))
                            ##se genera un tiempo aleatorio en el que estara en el I/O
                            tI_O=random.randint(1,10)
                            yield env.timeout(tI_O)
                            tOut=env.now
                            ##se sale del estado I/O y se regresa a seguir ejecutando instrucciones
                            print('el proceso %s salio del estado I/O en el tiempo %s'%(nombre,tOut))

##se pide el ingreso de los datos importantes para la utilizacion del programa
print('Bienvenido al programa')
procesos=input('ingrese la cantidad de procesos a ejecutar: ')
CPU=input('ingrese la cantidad de procesadores a utilizar: ')
RAM=100*(input('ingrese la cantidad de memoria ram: '))
cant=float(input('ingrese el intervalo en el que llegaran los procesos: '))
instruct=input('ingrese la cantidad de intrucciones a ejecutarse por vez: ')

##se inicia la simulacion
random.seed(seed)
env=simpy.Environment()
cpu=simpy.Resource(env,capacity=CPU)
i_o=simpy.Resource(env,capacity=1)
ram=simpy.Container(env,init=RAM,capacity=RAM)
env.process(fuente(env,cpu,i_o,ram,procesos,cant))
env.run()

##se obtiene el tiempo promedio y se imprime
promedio=tiempoTotal/procesos
print('-------------------------------')
print('promedio: %s'%(promedio))
print ('tiempo total: %s'%(tiempoTotal))
