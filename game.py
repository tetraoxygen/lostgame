#(c) 2016 Charlie Welsh, Foursoft. This program is under the GPLv3 license. Ver. σ1 THIS PROGRAM COMES WITH ABSOLUTELY NO WARRANTY.  Enjoy, Fourange.
import os


class Room(object):
    def __init__(self, r, exits=[],
                 desc="a perfect cube of a room. It is 2 meters cubed. There seems to be no way out.",
                 items=[],locks=[]):
        self.r=r
        self.exits=exits
        self.desc=desc
        self.items=items
        self.locks = locks

    def exits(self):
        if len(self.exits) == 0:
            return "nowhere."
        return self.exits

class Runtime(object):
    def __init__(self):
        self.roomlist = {}
        self.room = '0'
        self.readfile('level.txt')
        self.health=100
        self.inventory=[]

    def readfile(self,filename):
        f=open(filename)
        r = desc = None
        items = []
        locks=[]
        exits={}
        for line in f:
            line = line.rstrip('\n')
            if ':' in line:
                key, value = line.split(':')
                #print("key",key,"value",value)
                if key == 'desc':
                    desc = value
                if key == 'items':
                    if ',' in value:
                        values = value.split(',')
                    else:
                        values = [value]
                    items = values
                if key == 'locks':
                    if ',' in value:
                        values = value.split(',')
                    else:
                        values = [value]
                    locks = values
                if key == 'exits':
                    if ',' in value:
                        values = value.split(',')
                    else:
                        values = [value]
                    for val in values:
                        e_dir = val[0]
                        e_rm = val[2:]
                        print ("room",r,"dir", e_dir, "exit is", e_rm)
                        exits[e_dir] = e_rm
                if key == 'room':
                    print ("adding room")
                    if r is not None:
                        print ("adding previous room", r, "at", len(self.roomlist))
                        rm = Room(r, exits,desc,items,locks)
                        self.roomlist[r]=rm
                        r = desc = None
                        items = []
                        locks=[]
                        exits={}
                    r = value
        if r is not None:
            print ("adding last room", r, "at", len(self.roomlist))
            rm = Room(r, exits,desc,items,locks)
            self.roomlist[r]=rm
        f.close()
    
   
    def run(self):
        os.system('cls')
        while True:
            print("room:", self.room)
            print("You are in", self.roomlist[self.room].desc)
            print("items here:", self.roomlist[self.room].items)
            print("you are carrying:", self.inventory)
            if self.roomlist[self.room].locks is not None:
                print("the locked doors are:",  self.roomlist[self.room].locks)
            print("You can go", self.roomlist[self.room].exits)
            i = input(">").lower()
            cancel = 0
            if (i == 'unlock' or i == 'use key' or i == 'u') and 'key' in self.inventory:
                print('The door unlocks with a resounding clunk.')
                self.inventory.remove('key')
                self.roomlist[self.room].locks=[]
            elif(i == 'unlock' or i == 'use key' or i == 'u'):
                    print('There is no key in your inventory or there are no exits with locks in this room.')
                    cancel = 1 
            r = None
            if i == "t" or i == 'take':
                self.inventory.extend(self.roomlist[self.room].items)
                self.roomlist[self.room].items = []              
            elif i in ['n', 'north', 's', 'south', 'e', 'east', 'w', 'west']:
                dirname = i[0]
                if dirname in self.roomlist[self.room].exits:
                    if dirname in self.roomlist[self.room].locks:
                        print('That door is locked. Type U to unlock the door if you have a key.')
                    else:
                        r = self.roomlist[self.room].exits[dirname]
                else:
                    print('Invalid exit. Retry your command.')
            
            elif cancel == 0:
                print("That is invalid. Retype your command.")
                continue
                
            if r is not None:
                self.room=(r)


rt=Runtime()

rt.run()
