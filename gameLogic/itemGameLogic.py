import sympy as sp
import regex as re
from math import floor, ceil, log
import gamedefine
import gameLogic.numberLogic as numberLogic


def canAfford(item: str, doBuyMultiply = True) -> bool:
    """
    Checks if you can afford an item.

    Args:
        item (str): The item to check.

    Returns:
        bool: Whether you can afford the item or not.
    """
    
    buyMultiplier = gamedefine.mainTabBuyMultiple if doBuyMultiply else 1

    if gamedefine.itemInternalDefine[item]["costEquation"] == "":
        return True

    whatItCosts = gamedefine.itemInternalDefine[item]["whatItCosts"]
    
    ongoing = True
    
    for i in whatItCosts:
        if gamedefine.amounts[i["what"]] < i["amount"] * buyMultiplier:
            ongoing = False
    
    return ongoing

def purchase(item: str, doBuyMultiply = False) -> None:
    """
    Purchases an item.

    Args:
        item (str): The item to purchase.
        cost (int): The cost of the item.
    """

    buyMultiplier = gamedefine.mainTabBuyMultiple if doBuyMultiply else 1
    
    if gamedefine.itemInternalDefine[item]["costEquation"] == "":
        gamedefine.amounts[item] += 1
        print(f"purchased {item}, now have {gamedefine.amounts[item]}")
        return

    whatItCosts = gamedefine.itemInternalDefine[item]["whatItCosts"]
    whatItGives = gamedefine.itemInternalDefine[item]["whatItGives"]
    
    for i in whatItCosts:
        gamedefine.amounts[i["what"]] -= i["amount"] * buyMultiplier
    for i in whatItGives:
        gamedefine.amounts[i["what"]] += i["amount"] * buyMultiplier
    print(f"purchased {item}, now have {gamedefine.amounts[item]}")
    
    return

def getCurrentCost(item: str, _round : bool | None = False, eNotation : bool | None = True) -> dict:
    """
    Returns the current cost of an item.
    
    Args:
        item (str): The item to get the cost of.
        _round (bool | None): Whether to round the cost or not. Defaults to False.
    
    Returns:
        dict: The current cost of the item.    
    """
    
    buyMultiplier = gamedefine.mainTabBuyMultiple
    
    equation = gamedefine.itemInternalDefine[item]["costEquation"]
    if equation == "":
        return {"failed": True}

    whatItCosts = gamedefine.itemInternalDefine[item]["whatItCosts"][0]

    currentCost = int(numberLogic.evaluateCostEquation(equation, 1)) 

    if _round:
        return {whatItCosts: round(currentCost) * buyMultiplier}
    else: 
        return {whatItCosts: currentCost * buyMultiplier}
    


def parseCost(name):
    
    buyMultiplier = gamedefine.mainTabBuyMultiple
    
    if not name == "quarks":
        what = gamedefine.itemInternalDefine[name]["whatItCosts"]
        get = gamedefine.itemInternalDefine[name]["whatItGives"]
        string = ["Purchase "]                    
    else:
        return "Free"

    for i in get:
        string.append(str(i["amount"] * buyMultiplier) + " ")
        if i["amount"] * buyMultiplier == 1:
            string.append(i["what"][:-1])
        else:
            string.append(i["what"])
            
        if get.index(i) < len(get) - 2:
            string.append(", ")
        elif get.index(i) == len(get) - 2:
            string.append(" and ")
        else:
            string.append(" for ")

    for i in what:
        string.append(str(i["amount"] * buyMultiplier) + " ")
        if i["amount"] * buyMultiplier == 1:
            string.append(i["what"][:-1])
        else:
            string.append(i["what"])
            
        if what.index(i) < len(what) - 2:
            string.append(", ")
        elif what.index(i) == len(what) - 2:
            string.append(" and ")
        else:
            string.append(".")
    
    return "".join(string)



def maxAll():
    
    def maxAllPurchase(item):
        whatItCosts = gamedefine.itemInternalDefine[item]["whatItCosts"]
        whatItGives = gamedefine.itemInternalDefine[item]["whatItGives"]
        
        maxAmountPossible = 1
        
        for i in whatItCosts:
            maxAmountPossible = gamedefine.amounts[i["what"]] // i["amount"]
            
        for i in whatItCosts:
            gamedefine.amounts[i["what"]] -= i["amount"] * maxAmountPossible
        for i in whatItGives:
            gamedefine.amounts[i["what"]] += i["amount"] * maxAmountPossible

        
        print(f"max all purchased {maxAmountPossible} of {item}, now have {gamedefine.amounts[item]}")
        
        return
    
    affordList = []
    for i in gamedefine.itemInternalDefine:
        if not gamedefine.itemInternalDefine[i]["whatItCosts"][0]["what"] == "nothing":
            if i in gamedefine.purchaseToCreate:
                if canAfford(i, doBuyMultiply = False):
                    affordList.append(i)
    
    
    for i in affordList:
        maxAllPurchase(i) # this fixes the 'cascade effect' of the max all button by not actually purchasing it until the end

        