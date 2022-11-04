#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import time
import random
from datetime import datetime
from Funcoes import gerador_funcoes

username_gerador = "boo_gerador@jix.im"
username_mde = "boo_maquina_estados@jix.im"
username_resolvedor = "boo_resolvedor@jix.im"
password = "#Jujuba10"

dt = datetime.now()
dt.microsecond
random.seed(dt) #gera semente aleatoria


class Gerador(Agent):
    
    grau = random.randint(1,3)
    a, x,y = gerador_funcoes(grau)
 
    class funcao_grau(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=5)
            if res:
                x = float(res.body)
                
                if (Gerador.grau == 1):
                    x = float( Gerador.a*x + Gerador.y ) #envia de volta o valor de f(x)
                    print("Enviou para " + username_resolvedor  + " f(",res.body,")= ",x,"=>",int(x))
                elif Gerador.grau == 2:
                     x = float( Gerador.a*x**2 + Gerador.y ) #envia de volta o valor de f(x)
                     print("Enviou para " + username_resolvedor  + " f(",res.body,")= ",x,"=>",int(x))
                else: 
                     x = float( Gerador.a*x**3 + Gerador.y ) #envia de volta o valor de f(x)
                     print("Enviou para " + username_resolvedor  + " f(",res.body,")= ",x,"=>",int(x))
                     
                msg = Message(to=username_resolvedor ) 
                msg.set_metadata("performative", "inform")  
                msg.body = str(int(x))
                await self.send(msg)
                
                
    class tipo_funcao(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            print(str(msg))
            if msg:
                msg = Message(to=username_resolvedor) #se eu coloco msg.sender aqui não funciona, ele chama o gerador
                msg.set_metadata("performative", "inform")
                msg.body = str(Gerador.grau) + "grau"
                await self.send(msg)
                print("Respondeu para" + username_resolvedor + " com " + msg.body)
                

    async def setup(self):
        t = Template()
        t.set_metadata("performative","subscribe")

        tf = self.funcao_grau()
        
        if Gerador.grau == 1:
            print("Funcao de 1o grau: ", Gerador.x)
            print("Funcao: ", Gerador.a, "x + (", Gerador.y, ")")
        elif Gerador.grau == 2:
            print("Funcao de 2o grau: ", Gerador.x)
            print("Funcao: ", Gerador.a, "x² + (", Gerador.y, ")")
        else:
            print("Funcao de 3o grau: ", Gerador.x)
            print("Funcao: ", Gerador.a, "x³ + (", Gerador.y, ")")
            
        self.add_behaviour(tf,t) 
        

        ft = self.tipo_funcao()
        template = Template()
        template.set_metadata("performative", "request")
        self.add_behaviour(ft, template) #comportamento do tipo funcao
        

if __name__ == "__main__":
    time.sleep(5)
    gerador = Gerador("boo_gerador@jix.im", "#Jujuba10")
    gerador.web.start(hostname="127.0.0.1", port="10000")
    res = gerador.start()
    res.result()
      
    while gerador.is_alive():
       try:
          time.sleep(1)
       except KeyboardInterrupt:
          gerador.stop()
          break
    print("Agente encerrou!")
