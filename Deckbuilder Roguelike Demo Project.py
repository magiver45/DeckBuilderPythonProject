import random
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import Menu, Button, PhotoImage
from tkinter import messagebox as popup
from enum import Enum
from dataclasses import dataclass

# Cards!
class CardType(Enum): # Types of Cards
    ATTACK = "Deal _ Damage"
    DEFEND = "Gain _ Block"
    HEAL   = "Heal _ HP"
    STATUS = "Apply _ to _"

@dataclass
class CardFormat:
    card_name :str
    card_type :CardType
    card_cost :int
    card_value:int

class CardList(): # List Of All The Cards
    CT = CardType
    CF = CardFormat

    # Attack Cards
    slam  = CF( "Slam", CT.ATTACK, 0, 2)
    slash = CF("Slash", CT.ATTACK, 1, 5)
    stab  = CF( "Stab", CT.ATTACK, 1, 8)

    # Defense Cards
    block  = CF( "Block", CT.DEFEND, 0, 2)
    defend = CF("Defend", CT.DEFEND, 1, 5)
    parry  = CF( "Parry", CT.DEFEND, 1, 8)

    # Recovery Cards
    minor_heal = CF("Minor Heal", CT.HEAL, 1, 2)
    basic_heal = CF("Basic Heal", CT.HEAL, 2, 5)
    great_heal = CF("Great Heal", CT.HEAL, 2, 8)

    library = (slam, slash, stab, block, defend, parry, minor_heal, basic_heal)

# Characters!
class CharacterFormat(): # The Format Of The Characters
    def __init__(self, character_name:str, character_hp:int, character_max_hp:int, character_energy:int, character_defense:int, character_deck:tuple):
        self.character_name    = character_name
        self.character_hp      = character_hp
        self.character_max_hp  = character_max_hp
        self.character_energy  = character_energy
        self.character_defense = character_defense
        self.character_deck    = character_deck

class CharacterChoices(): # The Characters To Choose From
    CHF = CharacterFormat
    CL  = CardList

    barbarian = CHF("Barbarian", 100, 100, 3, 0, (CL.slam, CL.slam, CL.slam, CL.slash, CL.slash, CL.block, CL.block, CL.block, CL.defend, CL.defend))
    fighter   = CHF(  "Fighter",  80,  80, 3, 0, (CL.slash, CL.slash, CL.stab, CL.stab, CL.block, CL.block, CL.defend, CL.defend, CL.minor_heal, CL.minor_heal))
    cleric    = CHF(   "Cleric",  60,  60, 4, 5, (CL.slam, CL.slam, CL.slam, CL.block, CL.block, CL.defend, CL.defend, CL.minor_heal, CL.minor_heal, CL.basic_heal))
    player4   = CHF(  "player4",  40,  40, 3, 0, (CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam))#temp
    player5   = CHF(  "Player5",  20,  20, 2, 0, (CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam))#temp
    player6   = CHF(  "Player6",  20,  20, 2, 0, (CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam))#temp
    player7   = CHF(  "Player7",  20,  20, 2, 0, (CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam))#temp
    player8   = CHF(  "Player8",  20,  20, 2, 0, (CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam, CL.slam))#temp

    heroes = (barbarian, fighter, cleric, player4, player5, player6, player7, player8)

# Enemies!
class EnemyMoveType(Enum): # Types Of Enemy Moves
    ATTACK = "Attack"
    DEFEND = "Defend"
    BUFF   = "Buff Enemy"
    NERF   = "Nerf Player"

class EnemyMoveFormat(): # The Format Of Enemy Moves
    def __init__(self, move_name:str, move_type:EnemyMoveType, move_value:int):
        self.move_name  = move_name 
        self.move_type  = move_type
        self.move_value = move_value

class EnemyMoves(): # List Of Enemy Moves
    EMT = EnemyMoveType
    EMF = EnemyMoveFormat

    # Attack
    scratch = EMF("Scratch", EMT.ATTACK, 3)
    bite    = EMF(   "Bite", EMT.ATTACK, 5)

    # Defend
    prepare = EMF("Prepare", EMT.DEFEND, 3)

class EnemyFormat(): # The Format For Enemies
    def __init__(self, enemy_name:str, enemy_hp:int, enemy_max_hp:int, enemy_defense:int, enemy_moves:list):
        self.enemy_name    = enemy_name
        self.enemy_hp      = enemy_hp
        self.enemy_max_hp  = enemy_max_hp
        self.enemy_defense = enemy_defense
        self.enemy_moves   = enemy_moves

class EnemyList():
    EF = EnemyFormat
    EM = EnemyMoves

    giant_rat  = EF( "Giant Rat", 40, 40, 0, [EM.scratch, EM.scratch, EM.prepare])
    small_wolf = EF("Small Wolf", 60, 60, 0, [EM.scratch, EM.bite, EM.prepare])
    grey_wolf  = EF( "Grey Wolf", 80, 80, 5, [EM.bite, EM.prepare])

    bestiary = [giant_rat, small_wolf, grey_wolf]

# Game Logic
class GameLogic():
    def __init__(self):
        # Player
        self.player_character = None
        self.player_name      = str("No Name")
        self.player_hp        = int(0)
        self.player_max_hp    = int(0)
        self.player_energy    = int(0)
        self.player_block     = int(0)
        # Player's Cardsint
        self.player_deck      = []
        self.player_hand      = []
        self.player_discard   = []
        # Enemy
        self.enemy_creature   = None
        self.enemy_name       = str("No Name")
        self.enemy_hp         = int(0)
        self.enemy_max_hp     = int(0)
        self.enemy_block      = int(0)
        self.enemy_move       = str("Pending")
        # Turn Tracker
        self.whose_turn       = str("Player")
        self.turn_count       = int(1)

    def new_game_setup(self): # Sets up a new game
        player = self.player_character
        enemy  = self.new_enemy()

        # Resetting and setting up the Game
        self.player_name   = player.character_name
        self.player_hp     = player.character_hp
        self.player_max_hp = player.character_max_hp
        self.player_energy = player.character_energy
        self.player_block  = player.character_defense
        # Player's Cards
        self.player_deck      = list(player.character_deck)
        self.player_hand      = []
        self.player_discard   = []
        
        self.enemy_name   = enemy.enemy_name
        self.enemy_hp     = enemy.enemy_hp
        self.enemy_max_hp = enemy.enemy_max_hp
        self.enemy_block  = enemy.enemy_defense
        self.enemy_move   = random.choice(enemy.enemy_moves)

        self.shuffle_deck()
        self.starting_hand()

        print(self.player_name)
        print(self.enemy_name)        
        print(self.player_hand)

    def save_game(self):
        pass

    def load_game(self):
        pass

    def quit_game(self):
        GGUI.root.destroy()

    def new_enemy(self): # Picks an enemy
        return random.choice(EnemyList.bestiary)

    def shuffle_deck(self): # Shuffles the deck
        random.shuffle(self.player_deck)

    def starting_hand(self):
        for _ in range(3):
            self.player_hand.append(self.player_deck.pop())

    def draw_card(self): # draw a card from your deck
        if self.player_energy >=1:
            if len(self.player_hand) <= 7:
                if len(self.player_deck) == 0:
                    if len(self.player_discard) == 0:
                        popup.showinfo("No More Cards!")
                        return None
                    else:
                        self.shuffle_discard()
                self.player_energy -= 1
                self.player_hand.append(self.player_deck.pop())
            else:
                popup.showinfo("Your Hand Is Full!")
        else:
            popup.showinfo("Out Of Energy!")

    def shuffle_discard(self): # Puts the discard pile into the deck
        for _ in self.player_discard:
            self.player_deck.append(self.player_discard.pop())
            self.shuffle_deck()

    def play_card(self):
        card = None

    def enemy_turn(self): #Enemy Turn system
        self.whose_turn = "Enemy"

        if self.enemy_move.move_type == EnemyMoveType.ATTACK:
            move_damage = self.enemy_move.move_value - self.player_block
            if move_damage >= 1:
                self.player_hp -= move_damage
        elif self.enemy_move.move_type == EnemyMoveType.DEFEND:
            self.enemy_block += self.enemy_move.move_value

        self.enemy_move = random.choice(self.enemy_creature.enemy_moves)
        self.turn_count += 1
        self.whose_turn = "Player"

    def gain_card(self): # Adds a card to your deck
        self.player_deck.append(GameGUI.chosen_prize)

    def lose_card(self): # Removes a card from your deck
        pass # WIP

# Game Graphics
class GameGUI():
    def __init__(self, GL):
        self.game_logic = GL
        self.root = ttk.Window(themename="darkly")
        self.root.title("Deckbuilder Roguelike Demo Project")
        self.root.config(bg="black")
        self.root.geometry("800x450")
        self.root.minsize(400, 225)
        self.root.bind("<Configure>", self.window_resize)

        self.topbar_system()
        self.main_frame()
        
    # Systems
    def topbar_system(self):
        # Adds Topbar
        topbar = Menu(self.root)
        self.root.config(menu=topbar)

        # Top Bar Menu Logic
        file_menu = tk.Menu(   topbar, tearoff=False)
        save_menu = tk.Menu(file_menu, tearoff=False)
        load_menu = tk.Menu(file_menu, tearoff=False)

        # Topbar Menu Options
        topbar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label= "New Game", command=self.new_game)
        file_menu.add_cascade(label="Save Game", menu=save_menu)
        save_menu.add_command(label=   "Save 1", command=GL.save_game)
        save_menu.add_command(label=   "Save 2", command=GL.save_game)
        save_menu.add_command(label=   "Save 3", command=GL.save_game)
        file_menu.add_cascade(label="Load Game", menu=load_menu)
        load_menu.add_command(label=   "Load 1", command=GL.load_game)
        load_menu.add_command(label=   "Load 2", command=GL.load_game)
        load_menu.add_command(label=   "Load 3", command=GL.load_game)
        file_menu.add_separator()
        file_menu.add_command(label="Quit Game", command=GL.quit_game)

    def main_frame(self):
        self.frame = ttk.Frame(master = self.root)
        self.frame.grid(row=0,column=0)
        self.frame.propagate(False)
        self.frame.grid_propagate(False)

        test = ttk.Label(master = self.frame, text = "Testing...")
        test.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
    def window_resize(self, event):
        r_width = event.width
        r_height = event.height

        if (r_width / r_height) > (16/9):
            f_width = r_height * (16/9)
            f_height = r_height
        else:
            f_height = r_width / (16/9)
            f_width = r_width
        
        self.frame.config(width=f_width, height=f_height)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    # Game GUI
    def new_game(self):
        print("New Game Started") # Visual Test
        self.clear_frame(self.frame)
        pick_hero = CharacterChoices.heroes

        columns = 4

        for i, CHF in enumerate(pick_hero):
            row = i // columns
            col = i % columns
            hero_text = f"{CHF.character_name}\n HP: {CHF.character_max_hp}\n Energy: {CHF.character_energy}"
            btn = ttk.Button(self.frame, text=hero_text, command=lambda chosen=CHF : self.prep_game(chosen))
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def prep_game(self, chosen):
        self.clear_frame(self.frame)
        self.game_logic.player_character = chosen
        self.game_logic.new_game_setup()
        self.fight_hud()

    def fight_hud(self):
        player_info   = ttk.Label( self.frame, text=f"{self.game_logic.player_name} \n HP: {self.game_logic.player_hp} / {self.game_logic.player_max_hp} \n Energy: {self.game_logic.player_energy}")
        turn_tracker  = ttk.Label( self.frame, text=f"{self.game_logic.whose_turn}'s Turn \n Turn #{GL.turn_count}")
        enemy_info    = ttk.Label( self.frame, text=f"{self.game_logic.enemy_name} \n HP: {self.game_logic.enemy_hp} / {self.game_logic.enemy_max_hp} \n Incoming Attack: {self.game_logic.enemy_move.move_name}")
        card_counters = ttk.Label( self.frame, text=f"Deck:{len(self.game_logic.player_deck)} \n Discard:{len(self.game_logic.player_discard)}")
        draw_card     = ttk.Button(self.frame, text=f"Draw Card", command=self.game_logic.draw_card)
        end_turn      = ttk.Button(self.frame, text="End Turn", command=self.game_logic.enemy_turn)

        player_info.grid(  row=0, column=0, padx=1, pady=1, sticky="nsew")
        turn_tracker.grid( row=0, column=4, padx=1, pady=1, sticky="nsew")
        enemy_info.grid(   row=0, column=9, padx=1, pady=1, sticky="nsew")
        card_counters.grid(row=1, column=0, padx=1, pady=1, sticky="nsew")
        draw_card.grid(    row=2, column=9, padx=1, pady=1, sticky="nsew")
        end_turn.grid(     row=3, column=9, padx=1, pady=1, sticky="nsew")

        self.show_hand()

    def show_hand(self):
        for i, card in enumerate(self.game_logic.player_hand):
            card_text = f"{card.card_name} \n Cost:{card.card_cost} \n {self.card_description(card)}"
            card_button = ttk.Button(self.frame, text=card_text, command=None)
            card_button.grid(row=3, column=i, padx=5, pady=5, sticky="nsew")

    def card_description(self, _):
        if _.card_type.name == "ATTACK":
            return f"Deal {_.card_value} Damage"
        if _.card_type.name == "DEFEND":
            return f"Gain {_.card_value} Block"
        if _.card_type.name == "HEAL":
            return f"Heal {_.card_value} HP"
        else:
            popup.showinfo("Invalid Card!")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    GL   = GameLogic()
    GGUI = GameGUI(GL)
    GGUI.run()