from random import randint
class Dice(object):
    #a dice returns a random value of 1-6
    def __init__(self):
        self.value = randint(1, 6)
class Territory(object):
    #support for later
    #a territory has neighbors
    #a territory can only be attacked from its neighbors
    #a territory has an owner
    #a territory has a number of units for army
    pass
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
        fight = self.battle(attacker, defender)
###
#main program
###
LetsPlay = Game()
while True:
    LetsPlay.fight()
