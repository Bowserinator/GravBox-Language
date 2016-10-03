"""Python implmentation of https://esolangs.org/wiki/Gravbox"""
from __future__ import print_function
import random, time

def run( code, timeout = 999999 ): #Runs code
    start = time.time()
    stack = [] #The output stack 
    grav_direction = 0 #0 is down 1 is right 2 is up 3 is left
    quit = False
    returned = ""
    
    code = [list(c) for c in code.split("\n")]
    
    ball_cords = [] #Get the coordinates of all the balls
    for y in range(0, len(code)):
        for x in range(0, len(code[y])):
            if code[y][x] == "`":
                ball_cords.append([x,y])
                
    while not quit:
        #Update all the ball coordinates, run commands as hit
        for c in range(0,len(ball_cords)):
            if grav_direction == 0: #Down gravity
                try: 
                    if code[ball_cords[c][1] + 1][ball_cords[c][0]] == "#": pass
                    else: ball_cords[c][1] += 1
                except Exception as e: 
                    ball_cords[c][1] += 1
            elif grav_direction == 1: #Right gravity
                try: 
                    if code[ball_cords[c][1]][ball_cords[c][0] + 1] == "#": pass
                    else: ball_cords[c][0] += 1
                except Exception as e: 
                    ball_cords[c][0] += 1
            elif grav_direction == 2: #Up gravity
                try: 
                    if code[ball_cords[c][1] - 1][ball_cords[c][0]] == "#": pass
                    else: ball_cords[c][1] -= 1
                except Exception as e: 
                    ball_cords[c][1] -= 1
            elif grav_direction == 3: #Left gravity
                try: 
                    if code[ball_cords[c][1]][ball_cords[c][0] - 1] == "#": pass
                    else: ball_cords[c][0] -= 1
                except Exception as e: 
                    ball_cords[c][0] -= 1
                    
            if time.time() - start > timeout*1000:
                return "TIMEOUT"
        
        for x in range(0,len(ball_cords)): #Run commands:
            c = ball_cords[x]
            try:
                cmd = code[c[1]][c[0]]
                if cmd == "@": #Counter-clockwise switch gravity
                    grav_direction = (grav_direction+1)%4
                elif cmd == "/": #Bounce right
                    ball_cords[x][0] += 1
                elif cmd == "\\": #Bounce left
                    ball_cords[x][0] -= 1
                elif cmd == "!": #Invert stack item
                    if int(stack[0]) == stack[0]:
                        stack[0] =  stack[0]*-1 
                    else: pass 
                elif cmd in "1234567890": #Add number to stack
                    stack.append( int(cmd) )
                elif cmd == "+":
                    try: 
                        stack.append( int(stack[0]) + int(stack[1]) )
                        del stack[0]; del stack[0]
                    except: pass
                elif cmd == "-":
                    try: 
                        stack.append( int(stack[0]) - int(stack[1]) )
                        del stack[0]; del stack[0]
                    except: pass
                elif cmd == "*":
                    try: 
                        stack.append( int(stack[0]) * int(stack[1]) )
                        del stack[0]; del stack[0]
                    except: pass
                elif cmd == "|":
                    try: 
                        stack.append( int(stack[0]) / int(stack[1]) )
                        del stack[0]; del stack[0]
                    except: pass
                elif cmd == ".":
                    try: 
                        if type(stack[-1]) == int:
                           returned += chr(stack[-1])
                        else:
                            returned += stack[-1]
                        del stack[-1]
                    except: pass
                elif cmd == "^":
                    try: stack.append( stack[0] )
                    except: pass
                elif cmd == "%":
                    try: del stack[0]
                    except: pass
                elif cmd.lower() in "abcdefghijklmnopqrstuvwxyz":
                    stack.append(cmd)
                elif cmd == "?":
                    ball_cords[x][0] += random.choice([-1,1])
                elif cmd == "&":
                    try:
                        if stack[0] > 0:
                            ball_cords[x][0] += 1
                        else: 
                            ball_cords[x][0] -= 1
                    except: pass
                elif cmd == "$":
                    stack.append( len(stack) )
                elif cmd == "~":
                    quit = True
                elif cmd == ":":
                    try:
                        stack[0],stack[-1] = stack[-1],stack[0]
                    except: pass

                #code[c[1]][c[0]] = "" #Destroy the command!
            except: #Code index doesn't exist!!
                pass
        
        if time.time() - start > timeout*1000:
            return "TIMEOUT"
        #quit = True
                
    return returned
