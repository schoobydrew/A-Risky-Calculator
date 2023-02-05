from random import randint
import json
from collections import Counter

class Roll:
    def __init__(self,forces):
        num_dice = sum(v for v in forces.values())
        num_dice = num_dice - 1 if "aa_gun" in forces else num_dice
        self.outcome = sorted([randint(1,6) for i in range(num_dice)])
    def __str__(self):
        return f"Roll({self.outcome})"
    def __repr__(self):
        return f"Roll({self.outcome})"

def current_stats(a,d,m=None):
    print(f"Attacker forces: {a['forces']}")
    print(f"\tAttacker order: {a['order']}")
    print(f"Defender forces: {d['forces']}")
    print(f"\tDefender order: {a['order']}")
    print(f"Mapping {m}") if m else None
def remove_empty(forces):
    return {k:v for k,v in forces.items() if v > 0}


def precombat(attacker,defender,mapping):
    attacker_boats = {}
    attacker_aircraft = {}
    defender_boats = {}
    if "aa_gun" in defender["forces"]:
        attacker_aircraft = {
            "fighter":attacker["forces"].get("fighter",0),
            "bomber":attacker["forces"].get("bomber",0),
            "tactical_bomber":attacker["forces"].get("tactical_bomber",0)
        }
        aa_roll = Roll(attacker_aircraft)
        print(f"AA: {aa_roll}")
        aa_roll_hits = len([r for r in aa_roll.outcome if r <= mapping["defender"]["aa_gun"]])
        print(f"AA Gun hits: {aa_roll_hits}")
        available_units = []
        for unit in attacker["order"]:
            available_units += [unit]*attacker_aircraft.get(unit,0)
        while aa_roll_hits > 0 and available_units:
            aa_roll_hits -= 1
            cur_unit = available_units.pop(0)
            print(f"AA Destroyed: {cur_unit}")
        attacker_aircraft = {k:0 for k in attacker_aircraft}
        attacker_aircraft.update(Counter(available_units))
    if ("submarine" in defender["forces"]) and ("destroyer" not in attacker["forces"]):
        boats = {
            "submarine":attacker["forces"].get("submarine",0),
            "destroyer":attacker["forces"].get("destroyer",0),
            "cruiser":attacker["forces"].get("cruiser",0),
            "damaged_battleship":attacker["forces"].get("damaged_battleship",0),
            "battleship":attacker["forces"].get("battleship",0),
            "aircraft_carrier":attacker["forces"].get("aircraft_carrier",0),
            "damaged_aircraft_carrier":attacker["forces"].get("damaged_aircraft_carrier",0)
        }
        sub_roll = Roll({"submarine":defender["forces"]["submarine"]})
        sub_hits = len([r for r in sub_roll.outcome if r <= mapping["defender"]["submarine"]])
        print(f"Defending Sub: {sub_roll}")
        print(f"Defending Submarine hits: {sub_hits}")
        available_units = []
        for unit in attacker["order"]:
            available_units += [unit]*boats.get(unit,0)
        while sub_hits > 0 and available_units:
            sub_hits -= 1
            cur_unit = available_units.pop(0)
            print(f"Submarine hit: {cur_unit}")
            if cur_unit in ["battleship","aircraft_carrier"]:
                available_units = [f"damaged_{cur_unit}"] + available_units
        attacker_boats = {k:0 for k in boats}
        attacker_boats.update(Counter(available_units))
    if ("submarine" in attacker["forces"]) and ("destroyer" not in defender["forces"]):
        boats = {
            "submarine":defender["forces"].get("submarine",0),
            "destroyer":defender["forces"].get("destroyer",0),
            "cruiser":defender["forces"].get("cruiser",0),
            "damaged_battleship":defender["forces"].get("damaged_battleship",0),
            "battleship":defender["forces"].get("battleship",0),
            "aircraft_carrier":defender["forces"].get("aircraft_carrier",0),
            "damaged_aircraft_carrier":defender["forces"].get("damaged_aircraft_carrier",0)
        }
        sub_roll = Roll({"submarine":attacker["forces"]["submarine"]})
        sub_hits = len([r for r in sub_roll.outcome if r <= mapping["attacker"]["submarine"]])
        print(f"Attacking Sub: {sub_roll}")
        print(f"Attacking submarine hits: {sub_hits}")
        available_units = []
        for unit in defender["order"]:
            available_units += [unit]*boats.get(unit,0)
        while sub_hits > 0 and available_units:
            sub_hits -= 1
            cur_unit = available_units.pop(0)
            print(f"Submarine hit: {cur_unit}")
            if cur_unit in ["battleship","aircraft_carrier"]:
                available_units = [f"damaged_{cur_unit}"] + available_units
        defender_boats = {k:0 for k in boats}
        defender_boats.update(Counter(available_units))
    attacker["forces"].update(attacker_boats)
    attacker["forces"].update(attacker_aircraft)
    defender["forces"].update(defender_boats)
def combat(attacker,defender,mapping):
    attacker_forces = attacker["forces"]
    defender_forces = defender["forces"]
    # generate attacker mapping
    attacker_mapping = []
    for unit,value in attacker_forces.items():
        if unit in ["infantry","mechanized_infantry","tactical_bomber"]:
            continue
        attacker_mapping += [mapping["attacker"][unit]]*value
    num_infantry = attacker_forces.get("infantry",0) + attacker_forces.get("mechanized_infantry",0)
    if num_infantry > 0:
        attacker_mapping += [mapping["attacker"]["infantry"]]*(num_infantry - attacker_forces["artillery"])
        attacker_mapping += [mapping["attacker"]["artillery"]]*min(attacker_forces.get("artillery",0),num_infantry)
    num_tac_bomber = attacker_forces.get("tactical_bomber",0)
    if num_tac_bomber > 0:
        num_tanks_and_fighters = attacker_forces.get("tank",0) + attacker_forces.get("fighter",0)
        attacker_mapping += [mapping["attacker"]["tactical_bomber"]]*(num_tac_bomber-num_tanks_and_fighters)
        attacker_mapping += [4]*min(num_tanks_and_fighters,num_tac_bomber)
    attacker_mapping = sorted(attacker_mapping)
    # generate defender mapping
    defender_mapping = []
    for unit,value in defender_forces.items():
        if unit == "aa_gun":
            continue
        defender_mapping += [mapping["defender"][unit]]*value
    defender_mapping = sorted(defender_mapping)
    # roll for attacker
    attacker_roll = Roll(attacker_forces)
    print(f"Attacker map:  {attacker_mapping}")
    print(f"Attacker roll: {attacker_roll.outcome}")
    # roll for defender
    defender_roll = Roll(defender_forces)
    print(f"Defender map:  {defender_mapping}")
    print(f"Defender roll: {defender_roll.outcome}")
    # flatten attacker forces
    attacker_stack = []
    for unit in attacker["order"]:
        attacker_stack += [unit]*attacker_forces.get(unit,0)
    # flatten defender forces
    defender_stack = []
    for unit in defender["order"]:
        defender_stack += [unit]*defender_forces.get(unit,0)
    # process attacker results
    attacker_hits = 0
    for r in attacker_roll.outcome:
        for m in attacker_mapping:
            if r<=m:
                attacker_mapping.remove(m)
                attacker_hits += 1
                break
    # process defender results
    defender_hits = 0
    for r in defender_roll.outcome:
        for m in defender_mapping:
            if r<=m:
                defender_mapping.remove(m)
                defender_hits += 1
                break
    # apply attacker hits
    print(f"Attacker hits: {attacker_hits}")
    while attacker_hits > 0 and defender_stack:
        attacker_hits -= 1
        cur_unit = defender_stack.pop(0)
        print(f"Attacker hits: {cur_unit}")
        if cur_unit in ["battleship","aircraft_carrier"]:
            defender_stack = [f"damaged_{cur_unit}"] + defender_stack
    # apply defender hits
    print(f"Defender hits: {defender_hits}")
    while defender_hits > 0 and attacker_stack:
        defender_hits -= 1
        cur_unit = attacker_stack.pop(0)
        print(f"Defender hits: {cur_unit}")
        if cur_unit in ["battleship","aircraft_carrier"]:
            attacker_stack = [f"damaged_{cur_unit}"] + attacker_stack
    # update tables
    attacker_update = {unit:0 for unit in attacker["order"]}
    attacker_update.update(Counter(attacker_stack))
    attacker["forces"].update(attacker_update)
    defender_update = {unit:0 for unit in defender["order"]}
    defender_update.update(Counter(defender_stack))
    defender["forces"].update(defender_update)
if __name__ == "__main__":
    a = json.load(open("attacker.json"))
    d = json.load(open("defender.json"))
    m = json.load(open("mapping.json"))
    a["forces"] = remove_empty(a["forces"])
    d["forces"] = remove_empty(d["forces"])
    current_stats(a,d)
    input("---Attacker wishes to continue?---")
    precombat(a,d,m)
    while True:
        a["forces"] = remove_empty(a["forces"])
        d["forces"] = remove_empty(d["forces"])
        combat(a,d,m)
        a["forces"] = remove_empty(a["forces"])
        d["forces"] = remove_empty(d["forces"])
        current_stats(a,d)
        if (len(set(d["order"]) & set(d["forces"].keys())) == 0) or (len(set(a["order"]) & set(a["forces"].keys())) == 0):
            print("---FIGHT OVER---")
            break
        input("---Attacker wishes to continue?---")