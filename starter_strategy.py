from fcntl import LOCK_WRITE
from turtle import position

# import numpy as np
from game import player_state
from game import game_state
from util import utility
from random import Random
from game.game_state import GameState
import game.character_class

from game.item import Item

from game.position import Position
from strategy.strategy import Strategy

class StarterStrategy(Strategy):
    def strategy_initialize(self, my_player_index: int):
    
        return game.character_class.CharacterClass.WIZARD

    def move_action_decision(self, game_state: GameState, my_player_index: int) -> Position:
        

        return toCenter(game_state, my_player_index)

    def attack_action_decision(self, game_state: GameState, my_player_index: int) -> int:
        return Random().randint(0, 3)

    def buy_action_decision(self, game_state: GameState, my_player_index: int) -> Item:
        return Item.NONE

    def use_action_decision(self, game_state: GameState, my_player_index: int) -> bool:
        return False



def toCenter(game_state: GameState, my_player_index: int):
    curr  = game_state.player_state_list[my_player_index].position
    # 4 4
    # 4 5
    # 5 4
    # 5 5
    center = [Position(4, 5), Position(5, 4), Position(4, 4), Position(5, 5)]
    min = 0
    min_i = 0
    for i in range(len(center)):
        if (utility.manhattan_distance(center[i], curr) < min):
            min = utility.manhattan_distance(center[i], curr)
            min_i = i
    return center[min_i]


def attackLowest(game_state: GameState, my_player_index: int):
    in_range = getPlayerInRange(game_state, my_player_index)
    lowest = 0
    lowest_idx = 0
    for i in range(len(in_range)):
        player =game_state.player_state_list[in_range[i]]
        if player.health < lowest:
            lowest = player.health
            lowest_idx = in_range[i]
    # if (lowest_i == my_player_index) {
    #     for i in range(4):

    #         if i < 4:
    # }
    if (lowest_idx == my_player_index):
        return lowest_idx + 1
    return lowest_idx

def attackLowest(game_state: GameState, my_player_index: int):
    in_range = getPlayerInRange(game_state, my_player_index)
    highest = 0
    highest_idx = 0
    for i in range(len(in_range)):
        player =game_state.player_state_list[in_range[i]]
        if player.health > highest:
            highest = player.health
            highest_idx = in_range[i]
    # if (lowest_i == my_player_index) {
    #     for i in range(4):

    #         if i < 4:
    # }
    if (highest_idx == my_player_index):
        return highest_idx + 1
    return highest_idx


def getPlayerInRange(game_state: GameState, my_player_index: int):
    me  = game_state.player_state_list[my_player_index]
    range = me.stat_set.range
    li = []
    for p in range(len(game_state.player_state_list)):
        
        if (p == my_player_index):
            continue
        player = game_state.player_state_list[p]
        if utility.chebyshev_distance(me.position, player.position) <= range:
            li.append(p)

    return li


def kite(game_state: GameState, my_player_index):
    # for ranger
    vector = Position(0, 0)
    curr_pos = game_state.player_state_list[my_player_index].position
    total = 0
    for p in range(len(game_state.player_state_list)):
        player = game_state.player_state_list[p]

        direction = Position(0, 0)
        direction.x = curr_pos.x - player.position.x
        direction.y = curr_pos.y - player.position.y

        weight = player.stat_set.damage + player.stat_set.range + player.stat_set.speed
        total += weight
        # direction.x *= weight
        # direction.y *= weight

        vector.x += direction.x * weight
        vector.y += direction.y * weight
        
    l = utility.manhattan_distance(position(0, 0), vector)
    vector.x = vector.x / l * game_state.player_state_list[my_player_index].stat_set.range
    vector.y = vector.y / l * game_state.player_state_list[my_player_index].stat_set.range

    curr_pos.x += vector.x
    curr_pos.y += vector.y

    

    return curr_pos


