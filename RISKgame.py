from random import randint
players = ["red", "green", "blue"]
territories = ["TopLeft", "TopMid", "TopRight", "MidLeft", "MidMid", "MidRight", "LowLeft", "LowMid", "LowRight"]
class Dice(object):
    #a dice returns a random value of 1-6
    def __init__(self):
        self.value = randint(1, 6)
class Territory(object):
    #a territory has a name
    #a territory has neighbors
    #a territory can only be attacked from its neighbors
    #a territory has an owner
    #a territory has a number of units for army
    def __init__(self, name):
        self.name = name
        self.owner = None
        self.neighbors = []
class Player(object):
    #a player has up to 3 dice for each engagements
    def __init__(self, number):
        self.units = number
    #game will need a mutator to make sure they arent rolling with more than possible units
class Game(object):
    #the game should initiliaze with randomized distribution of territory
    #game has turns
    def __init__(self):
        pass
    #create territories
    #world is a dictionary with name of territory and territory itself
    def genesis(self):
        world = {}
        for i in territories:
            world[i] = Territory(i)
        #instantiate with neighbors
        #for this case we are building the world it would be possible to do
        # X X X X X
        # X O O O X
        # X O O O X
        # X O O O X
        # X X X X X
        # X is null and then neighbors are O location [+1, +5, -1, -5]
        # X could provide a buffer
        # I choose not to automate this generation bc this is a proof of concept for someone else to make a world map if they want
        world["TopLeft"].neighbors = ["TopMid", "MidLeft"]
        world["TopMid"].neighbors = ["TopLeft", "TopRight", "MidMid"]
        world["TopRight"].neighbors = ["TopMid", "MidRight"]
        world["MidLeft"].neighbors = ["TopLeft", "MidMid", "LowLeft"]
        world["MidMid"].neighbors = ["TopMid", "MidLeft", "MidRight", "LowMid"]
        world["MidRight"].neighbors = ["TopRight", "MidMid", "LowRight"]
        world["LowLeft"].neighbors = ["MidLeft", "LowMid"]
        world["LowMid"].neighbors = ["LowLeft", "MidMid", "LowRight"]
        world["LowRight"].neighbors = ["LowMid", "MidRight"]
        return world
    #determines roll outcome for a player
    def roll(self, a):
        roll_outcome = []
        for i in range(a):
            d = Dice()
            roll_outcome.append(d.value)
        roll_outcome.sort(reverse=True)
        return roll_outcome
    #takes each roll outcome
    def rolls(self, a, b):
        attacker_outcome = self.roll(a)
        defender_outcome = self.roll(b)
        return attacker_outcome, defender_outcome
    #evaluates the rolls to see who wins
    def battle(self, attacker, defender):
        attacker_outcome, defender_outcome = self.rolls(attacker.units, defender.units)
        battle_outcome = []
        aLose = 0
        bLose = 0
        for i in range(len(defender_outcome)):
            if defender_outcome[i] >= attacker_outcome[i]:
                battle_outcome.append("D")
                aLose += 1
            else:
                battle_outcome.append("A")
                bLose += 1
        print "A: {}".format(attacker_outcome)
        print "W: {}".format(battle_outcome)
        print "D: {}".format(defender_outcome)
        print "Attacker loses: {}".format(aLose)
        print "Defender loses: {}".format(bLose)
    def fight(self):
        attacker = Player(int(raw_input("How many do you want to attack with? ")))
        defender = Player(int(raw_input("How many do you want to defend with? ")))
        skirmish = self.battle(attacker, defender)
    def play(self):
        world = self.genesis()
        while True:
            for i in players:
                #addition phase
                while True:
                    break
                #fight phase
                while True:
                    player_input = raw_input("OOF: ")
                    if (player_input == "fight"):
                        self.fight()
                        break
                    else:
                        print "mine, world, fight, skip"
                #fortify phase
                while True:
                    break
###
#main program
###
LetsPlay = Game()
while True:
    LetsPlay.play()
