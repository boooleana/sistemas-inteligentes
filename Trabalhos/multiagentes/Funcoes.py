#!/usr/bin/env python3
# -*- coding: utf-8 -*-




import random 

def gerador_funcoes(n):
    
    
    x = random.randint(-1000,1000) 
    a=0
    while a == 0:
        a = random.randint(-100,100)
         
    if n == 1:
        y = -1 * (a*x)
  
    
    elif n == 2:
        y = -1 * (a*x**2)

        
    else: 
        y = -1 * (a*x**3)
        
    return a,x,y      




