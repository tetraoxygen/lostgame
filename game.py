#(c) 2016 Charlie Welsh, Foursoft. This program is under the Creative Commons Zero license. THIS PROGRAM COMES WITH ABSOLUTELY NO WARRANTY.  Enjoy, Fourange.
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
        self.roomlist = []
        self.room = 0
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
                print("key",key,"value",value)
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
                        e_rm = int(val[2])
                        print ("room",r,"dir", e_dir, "exit is", e_rm)
                        exits[e_dir] = e_rm
                if key == 'room':
                    print ("adding room")
                    if r is not None:
                        print ("adding previous room", r, "at", len(self.roomlist))
                        rm = Room(r, exits,desc,items,locks)
                        self.roomlist.append(rm)
                        r = desc = None
                        items = []
                        locks=[]
                        exits={}
                    r = int(value)
        if r is not None:
            print ("adding last room", r, "at", len(self.roomlist))
            rm = Room(r, exits,desc,items,locks)
            self.roomlist.append(rm)
        f.close()
    
   
    def run(self):
        while True:
            print("room:", self.room)
            print("You are in", self.roomlist[self.room].desc)
            print("items here:", self.roomlist[self.room].items)
            print("you are carrying:", self.inventory)
            if self.roomlist[self.room].locks is not None:
                print("the locked doors are:",  self.roomlist[self.room].locks)
            print("You can go", self.roomlist[self.room].exits)
            i = input(">").lower()
            r = None
            if i == "t" or i == 'take':
                self.inventory.extend(self.roomlist[self.room].items)
                self.roomlist[self.room].items = []              
            elif i in ['n', 'north', 's', 'south', 'e', 'east', 'w', 'west']:
                dirname = i[0]
                if dirname in self.roomlist[self.room].exits:
                    if dirname in self.roomlist[self.room].locks:
                        print('That door is locked. Keys will be implemented in a future update. Good luck.')
                    else:
                        r = self.roomlist[self.room].exits[dirname]
                else:
                    print('Invalid exit. Retry your command.')
            else:
                print("That is invalid. Retype your command.")
                continue
            if r is not None:
                self.room=int(r)


rt=Runtime()

rt.run()
