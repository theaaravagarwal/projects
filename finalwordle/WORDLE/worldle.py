#imports for the necessary libraries
import pygame as pg
import sys
import random
import time

#the word list to choose from
wordlist = [
    "abide",
    "acorn",
    "adore",
    "afire",
    "agile",
    "alien",
    "amble",
    "ample",
    "apple",
    "apron",
    "aquas",
    "arbor",
    "argue",
    "armor",
    "atlas",
    "audit",
    "auger",
    "aunts",
    "avert",
    "awake",
    "axial",
    "babes",
    "bacon",
    "badge",
    "baker",
    "banjo",
    "barge",
    "barks",
    "basin",
    "bathe",
    "beard",
    "beast",
    "beets",
    "begin",
    "belly",
    "bends",
    "berry",
    "bezel",
    "bible",
    "biker",
    "birds",
    "birth",
    "blaze",
    "bleed",
    "bliss",
    "blitz",
    "blues",
    "boast",
    "bones",
    "booth",
    "botch",
    "bound",
    "brace",
    "brave",
    "bribe",
    "brief",
    "broad",
    "broil",
    "brute",
    "bunch",
    "cabin",
    "cable",
    "cakes",
    "camps",
    "candy",
    "canoe",
    "capes",
    "cared",
    "cargo",
    "carve",
    "cello",
    "champ",
    "chaos",
    "charm",
    "cheek",
    "chews",
    "chief",
    "chips",
    "chops",
    "chump",
    "cinch",
    "clamp",
    "claps",
    "clash",
    "clerk",
    "cliff",
    "climb",
    "clips",
    "cloak",
    "clown",
    "clump",
    "coach",
    "coast",
    "couch",
    "crane",
    "crash",
    "crate",
    "crawl",
    "crisp",
    "crops",
    "crown",
    "cruel",
    "crush",
    "cubes",
    "cupid",
    "curve",
    "dairy",
    "dance",
    "darts",
    "deals",
    "dealt",
    "debit",
    "debut",
    "decay",
    "decor",
    "deeds",
    "deify",
    "delay",
    "delve",
    "demon",
    "dense",
    "dents",
    "depth",
    "diary",
    "dicey",
    "diggs",
    "diner",
    "diplo",
    "disco",
    "ditch",
    "diver",
    "dodge",
    "doily",
    "dolls",
    "donor",
    "douse",
    "dozen",
    "drape",
    "drawn",
    "dream",
    "dress",
    "drift",
    "drill",
    "drink",
    "drive",
    "drown",
    "drums",
    "dusty",
    "dwarf",
    "dwell",
    "eager",
    "eagle",
    "early",
    "earth",
    "easel",
    "eater",
    "eject",
    "elbow",
    "elder",
    "elite",
    "elude",
    "email",
    "empty",
    "enact",
    "ended",
    "enjoy",
    "enlist",
    "equal",
    "erase",
    "essay",
    "evade",
    "exact",
    "exalt",
    "exile",
    "exude",
    "fable",
    "faith",
    "faked",
    "fakes",
    "fancy",
    "farms",
    "fawns",
    "feast",
    "feeds",
    "feels",
    "fence",
    "ferns",
    "fetch",
    "fifty",
    "fight",
    "files",
    "firms",
    "flair",
    "flame",
    "flask",
    "flock",
    "flour",
    "flute",
    "foamy",
    "focal",
    "forge",
    "forms",
    "forty",
    "forum",
    "fours",
    "frail",
    "fraud",
    "fresh",
    "frogs",
    "front",
    "frost",
    "frown",
    "fruit",
    "fuels",
    "gains",
    "gears",
    "genus",
    "glare",
    "globe",
    "glows",
    "grace",
    "grain",
    "grave",
    "greed",
    "grief",
    "grind",
    "grows",
    "guard",
    "guess",
    "guide",
    "guilt",
    "gummy",
    "habit",
    "happy",
    "harms",
    "haste",
    "haunt",
    "havoc",
    "hazel",
    "heart",
    "heath",
    "heirs",
    "helix",
    "hello",
    "hinge",
    "hints",
    "honey",
    "hopes",
    "horns",
    "horse",
    "humer",
    "humid",
    "humor",
    "hunts",
    "hydra",
    "icily",
    "ideal",
    "idols",
    "image",
    "inane",
    "inbox",
    "index",
    "inert",
    "infer",
    "inlet",
    "input",
    "irons",
    "ivory",
    "jacks",
    "jaded",
    "jails",
    "jeans",
    "jewel",
    "jolly",
    "jumps",
    "karma",
    "keeps",
    "kicks",
    "kings",
    "knack",
    "knots",
    "label",
    "laced",
    "laces",
    "lakes",
    "laser",
    "latte",
    "laugh",
    "leafy",
    "leaks",
    "leaps",
    "leash",
    "least",
    "leave",
    "leech",
    "legal",
    "lends",
    "leper",
    "level",
    "lewis",
    "libra",
    "light",
    "lilac",
    "liver",
    "lives",
    "lofty",
    "lodge",
    "logic",
    "lunar",
    "lunch",
    "lungs",
    "lurch",
    "lyric",
    "magic",
    "maids",
    "maker",
    "mango",
    "maple",
    "marry",
    "marsh",
    "medal",
    "meets",
    "merry",
    "metal",
    "minds",
    "mines",
    "minus",
    "mixed",
    "mixes",
    "mocha",
    "moral",
    "moths",
    "mouse",
    "movie",
    "muffin",
    "music",
    "nails",
    "naive",
    "nanny",
    "nasal",
    "nasty",
    "navel",
    "necks",
    "nerds",
    "nests",
    "nicer",
    "niece",
    "nifty",
    "noble",
    "nodal",
    "noisy",
    "nomad",
    "nooks",
    "notch",
    "nudge",
    "nuked",
    "oasis",
    "ocean",
    "odder",
    "offer",
    "often",
    "okapi",
    "olive",
    "onion",
    "orbit",
    "orgas",
    "osier",
    "ounce",
    "paddy",
    "pains",
    "pales",
    "palms",
    "pants",
    "paris",
    "parks",
    "parts",
    "party",
    "pasta",
    "paste",
    "patio",
    "paved",
    "paves",
    "peace",
    "peaks",
    "pears",
    "penny",
    "perch",
    "petal",
    "pets",
    "piano",
    "pilaf",
    "pilgr",
    "pilot",
    "pique",
    "plaid",
    "plank",
    "plaza",
    "plead",
    "plots",
    "plush",
    "poach",
    "poems",
    "poked",
    "poker",
    "pokes",
    "polls",
    "pools",
    "poppy",
    "porch",
    "ports",
    "posed",
    "poses",
    "pound",
    "power",
    "pride",
    "prime",
    "probe",
    "proud",
    "prove",
    "puled",
    "pules",
    "punch",
    "purse",
    "quail",
    "quake",
    "quark",
    "quart",
    "queen",
    "quest",
    "quick",
    "quiet",
    "quota",
    "quote",
    "radar",
    "radio",
    "rails",
    "raise",
    "rakes",
    "rally",
    "ramps",
    "ranch",
    "rapid",
    "raven",
    "razor",
    "reach",
    "reads",
    "realm",
    "rebel"
]

#remove duplicates from the list
wordlist = list(set(wordlist))

#function to choose a random word from the list
def getrand():
    return random.choice(wordlist)

#init pygame
pg.init()

# Create a Pygame window
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Wordle")
FONT = pg.font.Font('Fonts/minecraft.ttf', 48)  #load a custom font (optional)
#note: if you want to have a standard font, just leave 'Fonts/minecraft.ttf' as None
fps = 60  #fps

# Define colors
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Initialize game variables
correctword = [n for n in getrand()] #choose a random word from the wordlist
attempts = 0
max_attempts = 6
past_results = []#used to store previous att

#its literally in the name
game_over_flag = False

#function animate the letters
def animate_letters(letter, color, x, y):
    #render letter with color
    letter_surface = FONT.render(letter, True, color)
    letter_rect = letter_surface.get_rect(center=(x, y))
    screen.blit(letter_surface, letter_rect)
    pg.display.flip()
    time.sleep(0.1)  #animation delay

#function to play an animation for a word
def play_animation(word, result):
    x_offset = 400 - (len(result) // 2) * 40
    y = 300
    for i, (letter, color) in enumerate(zip(word, result)):
        animate_letters(letter, color, x_offset + i * 40, y)

# def InputBox for text input
class InputBox:
    def __init__(self, x, y, w, h):
        #init input box
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = ''
        self.active = False
        self.letters = 0
        self.txt_surface = FONT.render(self.text, True, self.color)

    def handle_event(self, event):
        #handle events for input box
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

        if event.type == pg.KEYDOWN and event.key != pg.K_RSHIFT and event.key != pg.K_LSHIFT:
            if self.active and self.letters < 5:  #limit input to 5 letters
                if event.key == pg.K_RETURN and self.letters > 4:
                    result = wordlecheck(correctword, self.text)
                    past_results.append((self.text, result))
                    self.text = ''
                    self.letters = 0
                #handle backspace, alphabetical chars, and update text surface
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.letters -= 1
                elif self.letters < 5 and event.unicode.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    self.text += event.unicode
                    self.letters += 1
                self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        #draw input box
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pg.draw.rect(screen, self.color, self.rect, 2)

#function to check correctness of guessed word
def wordlecheck(correct, actual):
    result = []  #store result as list of colors
    min_length = min(len(correct), len(actual))  #find min len

    for n in range(min_length):
        if actual[n] not in correct:
            result.append(RED)  #not correct letter
        elif actual[n] == correct[n]:
            result.append(GREEN)  #correct letter
        elif actual[n] in correct:
            result.append(YELLOW)  #correct position but wrong letter

    result.extend([RED] * (len(correct) - min_length))  #red for extra

    return result

#function to display past results
def display_past_results():
    y = 100  #y pos
    for word, result in past_results:
        x_offset = 400 - (len(result) // 2) * 40
        for i, color in enumerate(result):
            letter_surface = FONT.render(word[i], True, color)
            letter_rect = letter_surface.get_rect(center=(x_offset + i * 40, y))
            screen.blit(letter_surface, letter_rect)
        y += 50  #spacing

#function for the game over screen
def game_over(correct_word):
    result_text = " ".join(correct_word)
    result_surface = FONT.render(f"Correct Word: {result_text}", True, GREEN)
    result_rect = result_surface.get_rect(center=(400, 450))
    screen.blit(result_surface, result_rect)
    pg.display.flip()
    pg.time.delay(2000)
    pg.quit()
    sys.exit()

#game loop
def main():
    global attempts
    attempts = 0

    clock = pg.time.Clock()
    input_box = InputBox(280, 500, 240, 60)
    input_boxes = [input_box]

    current_guess = ""

    global game_over_flag
    game_won = False

    while not game_over_flag:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over_flag = True
            for box in input_boxes:
                box.handle_event(event)

        if input_box.letters == 5 and not game_won:
            current_guess = input_box.text
            input_box.text = ''
            input_box.letters = 0
            input_box.txt_surface = FONT.render(input_box.text, True, input_box.color)

            attempts += 1
            result = wordlecheck(correctword, current_guess)
            past_results.append((current_guess, result))
            play_animation(current_guess, result)

            if result == [GREEN, GREEN, GREEN, GREEN, GREEN]:
                game_won = True
                display_game_won()
                pg.display.flip()
                pg.time.delay(1000)
                game_over_flag = True

            if attempts == max_attempts:
                game_over_flag = True

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        display_past_results()

        pg.display.flip()
        clock.tick(fps)

    if not game_won:
        game_over(correctword)

#function to display the game won message
def display_game_won():
    game_won_surface = FONT.render("You won the game!", True, GREEN)
    game_won_rect = game_won_surface.get_rect(center=(400, 450))
    screen.blit(game_won_surface, game_won_rect)

if __name__ == '__main__':
    main()  #start loop