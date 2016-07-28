#(c) 2016 Charlie Welsh, Foursoft. This program is under the GPLv3 license. Vσ1 THIS PROGRAM COMES WITH ABSOLUTELY NO WARRANTY.  Enjoy, Fourange.
import os
import random
import time

class Room(object):
    def __init__(self, r, exits=[],
                 desc="a perfect cube of a room. It is 2 meters cubed. There seems to be no way out.",
                 items=[],locks=[],npc=[],light=[]):
        self.r=r
        self.exits=exits
        self.desc=desc
        self.items=items
        self.locks = locks
        self.light = light
        self.npc = npc

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
        light='normal'
        npc = []
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
                if key == 'npc':
                    if ',' in value:
                        values = value.split(',')
                    else:
                        values = [value]
                    npc = values
                    print ("room",r,"creatures", npc)
                if key == 'locks':
                    if ',' in value:
                        values = value.split(',')
                    else:
                        values = [value]
                    locks = values
                if key == 'light':
                    light = value
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
                        rm = Room(r, exits,desc,items,locks,npc,light)
                        self.roomlist[r]=rm
                        r = desc = None
                        items = []
                        npc = []
                        locks=[]
                        light = 'normal'
                        exits={}
                    r = value
        if r is not None:
            print ("adding last room", r, "at", len(self.roomlist))
            rm = Room(r, exits,desc,items,locks,npc,light)
            self.roomlist[r]=rm
        f.close()
    
   
    def run(self):
        os.system('cls')
        while True:
            print("room:", self.room)
            isdark = self.roomlist[self.room].light == 'dark'
            if isdark and 'flashlight' in self.inventory:
                print("it's dark here, you turn on your flashlight")
                isdark = False
            if isdark and  not 'flashlight' in self.inventory:
                print("it's dark here, you can't see anything")
            else:
                print("You are in", self.roomlist[self.room].desc)
                print("items here:", self.roomlist[self.room].items)
                print("you are carrying:", self.inventory)
                print("the light is", self.roomlist[self.room].light)
                print("creatures in here:", self.roomlist[self.room].npc)
                print("You can go", self.roomlist[self.room].exits)
                if self.roomlist[self.room].locks is not None:
                    print("the locked doors are:",  self.roomlist[self.room].locks)
            i = input(">").lower()
            if 'Giant Spider' in self.roomlist[self.room].npc:
                print("There is a giant spider in the room!")
                self.attackSpider()
            if(i == 'e' or i == 'eat') and 'food' in self.inventory:
                self.inventory.remove('food')
                self.health = 100
                print("you now have 100 life")
            elif (i == 'unlock' or i == 'use key' or i == 'u') and 'key' in self.inventory:
                print('The door unlocks with a resounding clunk.')
                self.inventory.remove('key')
                self.roomlist[self.room].locks=[]
            elif(i == 'unlock' or i == 'use key' or i == 'u'):
                    print('There is no key in your inventory or there are no exits with locks in this room.')
            cancel = 1 
            r = None
            if i == "t" and not isdark:
                self.inventory.extend(self.roomlist[self.room].items)
                self.roomlist[self.room].items = []
            elif i == "t" and 'dark' in self.roomlist[self.room].light:
                print("This room is too dark to see, you need a flashlight.")
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
            else:
                cancel = 0 
            if r is not None:
                self.room=(r)

    def checkWeapon(self):
        if 'dagger' in self.inventory:
            return 15
        elif 'axe' in self.inventory:
            return 12
        else:
            return 3

    def attackSpider(self):
        print("YOU FIGHT THE SPIDER")
        fighting = True
        spiderHealth = 30
        if random.randint(1,2) == 1:
            self.health -=random.randint(0,10)
            print("your health:", self.health)
            print("spider health:", spiderHealth)
            if self.health <= 0:
                a = input("you died, do you try again, yes or no >").lower()
                fighting = False
                if a == "y" or a == 'yes':
                    self.health = 100
                    spiderHealth = 30
                    fighting = True
                else:
                    print("You lose")
                    while True:
                        print(" ")
        else:
            damageMX = self.checkWeapon()
            while fighting:
                time.sleep(0.5)
                spiderHealth -= random.randint(0,damageMX)
                print("your health:", self.health)
                print("spider health:", spiderHealth)
                if spiderHealth <= 0:
                    fighting = False
                    self.roomlist[self.room].npc.remove("Giant Spider")
                    print("you killed a spider")
                self.health -=random.randint(0,10)
                print("your health:", self.health)
                print("spider health:", spiderHealth)
                if self.health <= 0:
                    a = input("you died, do you try again, yes or no >").lower()
                    fighting = False
                    if a == "y" or a == 'yes':
                        self.health = 100
                        spiderHealth = 30
                        fighting = True
                    else:
                        print("You lose")
                        exit()


rt=Runtime()

rt.run()
