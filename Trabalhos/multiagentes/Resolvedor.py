#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import math

import time
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import FSMBehaviour, State, OneShotBehaviour


STATE_ONE = "STATE_ONE"
STATE_TWO = "STATE_TWO"
STATE_THREE = "STATE_THREE"
STATE_FOUR = "STATE_FOUR"
STATE_FIVE = "STATE_FIVE"

username_gerador = "18204402_gerador@jix.im"
username_mde = "18204402_maquina_estados@jix.im"
username_resolvedor = "18204402_resolvedor@jix.im"
password = "sistemas_inteligentes2020.2"

#requeste  --- pergunta qual o tipo de função para o gerador 
#subscribe 

class ExampleFSMBehaviour(FSMBehaviour):
    async def on_start(self):
        print(f"Iniciando a máguina de estados {self.current_state}")
            
    async def on_end(self):
        print(f"Máquina de estados terminou no estado {self.current_state}")
        await self.agent.stop()

class StateOne(State):
    async def run(self):
        print("Estado um, perguntando o tipo de funcao:")
        msg = Message(to=username_gerador)
        msg.set_metadata("performative", "request")
        msg.body = "Qual o tipo da funcao?"
        await self.send(msg)
        
        resposta = await self.receive(timeout=10)
        
        if resposta:
            print("recebeu a resposta")
            if resposta.body == "1grau":
                self.set_next_state(STATE_TWO)
            elif resposta.body == "2grau":
                self.set_next_state(STATE_THREE)
            else:
                self.set_next_state(STATE_FOUR)
                
        else:
            print("Nenhuma mensagem recebida")
        
        

class StateTwo(State): #resolve a funcao de primeiro grau
    async def run(self):
        
        print("Primeira iteração: x = 0")
        msg = Message(to=username_gerador)
        msg.set_metadata("performative", "subscribe")
        msg.body = str(0)
        await self.send(msg)
        
        resposta = await self.receive(timeout=10)
        valor0 = int(resposta.body)
       
        print("Segunda iteração: x = 1")
        msg = Message(to=username_gerador)
        msg.set_metadata("performative", "subscribe")
        msg.body = str(1)
        await self.send(msg)
        
        resposta = await self.receive(timeout=10)
        valor1 = int(resposta.body)
        
        x = valor0+(-1*valor1)
        
        print("Terceira iteração: x =", x)
        msg = Message(to=username_gerador)
        msg.set_metadata("performative", "subscribe")
        msg.body = str(x)
        await self.send(msg)
        
        resposta = await self.receive(timeout=10)     
          
        print("Uma raiz da funcao é o número:", x)    
        self.set_next_state(STATE_FIVE)
'''
resolve a funcao de segundo grau
'''
class StateThree(State): 
    async def run(self): 
        
        print("Primeira iteração: x = 0")
        msg = Message(to=username_gerador)
        msg.set_metadata("performative", "subscribe")
        msg.body = str(0)
        await self.send(msg)
        
        resposta = await self.receive(timeout=10)
        valor0 = int(resposta.body)
       
        print("Segunda iteração: x = 1")
        msg = Message(to=username_gerador)
        msg.set_metadata("performative", "subscribe")
        msg.body = str(1)
        await self.send(msg)
        
        resposta = await self.receive(timeout=10)
        valor1 = int(resposta.body)
        
        a = valor0 + (-1 *valor1)
        x = (valor0/a)**(1/2)
        
        print("Terceira iteração: x =", x)
        msg = Message(to=username_gerador)
        msg.set_metadata("performative", "subscribe")
        msg.body = str(x)
        await self.send(msg)
        
        resposta = await self.receive(timeout=10)     
          
        print("Uma raiz da funcao é o número:", x)    
        self.set_next_state(STATE_FIVE)

'''        
resolve a funcao de terceiro grau 
'''
class StateFour(State):
    async def run(self):
              
        print("Primeira iteração: x = 0")
        msg = Message(to=username_gerador)
        msg.set_metadata("performative", "subscribe")
        msg.body = str(0)
        await self.send(msg)
        
        resposta = await self.receive(timeout=10)
        valor0 = int(resposta.body)
       
        print("Segunda iteração: x = 1")
        msg = Message(to=username_gerador)
        msg.set_metadata("performative", "subscribe")
        msg.body = str(1)
        await self.send(msg)
        
        resposta = await self.receive(timeout=10)
        valor1 = int(resposta.body)
        
        a = valor0 + (-1 *valor1)
        x = (valor0/a)**(1/3)
        
        print("Terceira iteração: x =", x)
        msg = Message(to=username_gerador)
        msg.set_metadata("performative", "subscribe")
        msg.body = str(x)
        await self.send(msg)
        
        resposta = await self.receive(timeout=10)     
          
        print("Uma raiz da funcao é o número:", x)    
        self.set_next_state(STATE_FIVE)



class StateFive(State):
    async def run(self):
        print("Máquina de estados finalizada (final state)")
        time.sleep(10)
        

class FSMAgent(Agent):
    async def setup(self):
        fsm = ExampleFSMBehaviour()
        fsm.add_state(name=STATE_ONE, state=StateOne(), initial=True)
        fsm.add_state(name=STATE_TWO, state=StateTwo())
        fsm.add_state(name=STATE_THREE, state=StateThree())
        fsm.add_state(name=STATE_FOUR, state=StateFour())
        fsm.add_state(name=STATE_FIVE, state=StateFive())
        fsm.add_transition(source=STATE_ONE, dest=STATE_TWO)
        fsm.add_transition(source=STATE_ONE, dest=STATE_THREE)
        fsm.add_transition(source=STATE_ONE, dest=STATE_FOUR)
        fsm.add_transition(source=STATE_ONE, dest=STATE_FIVE)
        fsm.add_transition(source=STATE_TWO, dest=STATE_FIVE)
        fsm.add_transition(source=STATE_THREE, dest=STATE_FIVE)
        fsm.add_transition(source=STATE_FOUR, dest=STATE_FIVE)       
        
        self.add_behaviour(fsm)



if __name__ == "__main__":
    time.sleep(5)
    fsmagent = FSMAgent("18204402_resolvedor@jix.im", "sistemas_inteligentes2020.2")
    future = fsmagent.start()
    future.result()

    while fsmagent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            fsmagent.stop()
            break
        
    print("Agent finished")