from os import path
import re
from pathlib import Path
from classes.mastermind import Mastermind
from classes.colors import bcolors
from classes.saveprovider import SaveProvider

class ConsoleInterface:

    def __init__(self):
        self.SAVE_SLOTS = 4
        self.save_folder = path.join(str(Path.home()), 'kodtoro')

        self.save_provider = SaveProvider(self.SAVE_SLOTS, self.save_folder, 'mentes-{}.sav')
        self.mastermind = Mastermind()

    def show_intro(self):
        text = f'A klasszikus színkeresős táblajáték, a Mastermind játszható ezzel a programmal.\n\
            |Tippelni a színek kezdőbetűjével lehet:\n\n\
            |    {bcolors.BLUE}K{bcolors.ENDC}ék,\n\
            |    {bcolors.YELLOW}S{bcolors.ENDC}árga,\n\
            |    {bcolors.GREEN}Z{bcolors.ENDC}öld,\n\
            |    {bcolors.RED}P{bcolors.ENDC}iros,\n\
            |    {bcolors.ORANGE}N{bcolors.ENDC}arancs,\n\
            |    {bcolors.WHITE}F{bcolors.ENDC}ehér\n\n\
            |A négy betűt egymás után írva lehet tippelni\
            | (pl: {bcolors.GREEN}Z{bcolors.ENDC}{bcolors.RED}P{bcolors.ENDC}{bcolors.ORANGE}N{bcolors.ENDC}{bcolors.BLUE}K{bcolors.ENDC})\n\n\
            |Az S betűvel elmentheted, az L betűvel betöltheted, az X betűvel feladhatod a játékot.'
        print(re.sub("\\ {4,}\\|", '', text, flags=re.MULTILINE))

    def console_loop(self):
        self.show_intro()

        self.mastermind.new_game()
        self.exit_now = False
        while not self.exit_now:
            try:
                raw_input = input('Tipp: ').upper()
                match raw_input.upper():
                    case 'X':
                        print("A feladvány a következő volt:")
                        self.printout_pattern()
                        print("Viszlát! Köszönöm, hogy játszottál!")
                        self.exit_now = True
                    case 'S':
                        self.save_game()
                    case 'L':
                        self.load_game()
                    case 'G':
                        if self.mastermind.finish() or input('Valóban új játékot szeretnél kezdeni?[i/n] ').upper() == 'I':
                            print("Új játékot kezdtél.")
                            self.mastermind.new_game()
                    case _:
                        guess = self.analyze_input_as_guess(raw_input)
                        if guess is not False:
                            self.handle_guess(guess)
                        else:
                            print('Érvénytelen tipp: 4 szí')
            except Exception as e:
                print(f"{bcolors.RED}{str(e)}{bcolors.ENDC}")

    def analyze_input_as_guess(self, raw_input):
        chars = list(raw_input.replace(' ', '').upper())

        # hossz ellenőrzések
        if len(chars) > 4:
            raise Exception('Érvénytelen tipp: Túl sok színt adtál meg!')
        if len(chars) < 4:
            raise Exception('Érvénytelen tipp: Túl kevés színt adtál meg!')
        return chars

    def handle_guess(self, chars):
        if self.mastermind.finish():
            print("a játék már befejeződött. A G betűvel tudsz új játékot kezdeni.")
        else:
            guess = self.mastermind.validate_guess(chars)
            self.mastermind.guess(guess)
            self.printout()
            if self.mastermind.finish():
                if self.mastermind.won:
                    print("NYERTÉL!")
                else:
                    print('Nem sikerült kitalálnod a feladványt. :(')
                    print('A feladvány ez volt:')
                    self.printout_pattern()
                if input('Szeretnél új játékot  kezdeni?[i/n] ').upper() == 'I':
                    print("Új játékot kezdtél.")
                    self.mastermind.new_game()
                else:
                    self.exit_now = True

    def load_game(self):
        loaded = False

        while not loaded:
            slot_input = input(f'Hányas mentési helyet szeretnéd betölteni [1-{self.SAVE_SLOTS}, X mégse]?')
            if slot_input.upper() == 'X':
                print('Betöltés visszavonva.')
                self.printout()
                loaded = True
            else:
                if not slot_input.isnumeric():
                    print('Csak a mentési hely számát írd be!')
                else:
                    slot = int(slot_input)
                    if slot not in range(1, self.SAVE_SLOTS + 1):
                        print('Érvénytelen mentési hely!')
                    else:
                        data = self.save_provider.load(slot)
                        self.mastermind.deserialize(data)
                        # Az utolsó lépés kiértékelése
                        self.mastermind.finish()
                        loaded = True
                        print('Játék betöltve!')
                        self.printout()

    def save_game(self):
        if self.mastermind.finished:
            raise Exception('Csak játék közben lehet menteni!')

        saved = False
        while not saved:
            slot_input = input(f'Hányas mentési helyre szeretnél menteni [1-{self.SAVE_SLOTS}, X mégse]?')
            if slot_input.upper() == 'X':
                print('Mentés visszavonva.')
                self.printout()
                saved = True
            else:
                if not slot_input.isnumeric():
                    print('Csak a mentési hely számát írd be!')
                else:
                    slot = int(slot_input)
                    if slot not in range(1, self.SAVE_SLOTS + 1):
                        print('Érvénytelen mentési hely!')
                    else:
                        data = self.mastermind.serialize()
                        self.save_provider.save(slot, data)
                        saved = True
                        print('Játék elmentve!')

    def printout(self):
        i = 0
        for guess in self.mastermind.get_guesses():
            i += 1
            line = f"{i:>2}. "
            for color in guess['guess']:
                line += self.colorize(color, color)
                line += ' '
            line += self.colorize('PLACE_OK', str(guess['result']['place']))
            line += self.colorize('COLOR_OK', str(guess['result']['color']))

            print(line)

    def colorize(self, color, text):
        cols = {
            'K': bcolors.BLUE,
            'S': bcolors.YELLOW,
            'Z': bcolors.GREEN,
            'P': bcolors.RED,
            'N': bcolors.ORANGE,
            'F': bcolors.WHITE,
            'COLOR_OK': bcolors.WHITE,
            'PLACE_OK': bcolors.GREY,
        }
        reset = bcolors.ENDC

        return cols[color] + str(text) + reset

    def printout_pattern(self):
        pattern = self.mastermind.get_pattern()

        line = ''
        for color in pattern:
            line += self.colorize(color, color) + ' '
        print(line)
