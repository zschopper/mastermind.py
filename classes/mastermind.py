
import random

class Mastermind:

    def __init__(self):
        self.max_guesses = 10
        self.pattern = []
        self.guesses = []
        self.won = False
        self.finished = True
        self.valid_colors = (
            'K',  # Kék
            'S',  # Sárga
            'Z',  # Zöld
            'P',  # Piros
            'N',  # Narancs
            'F',  # Fehér
        )

    def validate_guess(self, chars):
        # többször megadott színek és érvénytelen betűk keresése
        prev = ''
        chars_sorted = chars.copy()
        chars_sorted.sort()
        for letter in chars_sorted:
            # ha a betű nincs az érvényes színek között - érvénytelen
            if letter not in self.valid_colors:
                raise Exception(F'Érvénytelen tipp: "{letter}" nem érvényes szín!')
            # ha már volt (sorrendbe rakott listán ugyanaz, mint az előző)
            if prev == letter:
                raise Exception('Érvénytelen tipp: Egy színt csak egyszer lehet használni!')
            prev = letter
        return chars

    def new_game(self):
        self.pattern = []
        self.guesses = []
        self.won = False
        self.finished = False
        while len(self.pattern) < 4:
            letter = self.valid_colors[random.randint(0, 5)]
            if letter not in self.pattern:
                self.pattern.append(letter)

    def check(self, guess=[]):
        color = 0
        place = 0
        for i in range(4):
            try:
                idx = guess.index(self.pattern[i])
                if idx == i:
                    place += 1
                else:
                    color += 1
            except ValueError:
                pass
        return {'place': place, 'color': color}

    def finish(self):
        if len(self.guesses) == 0:
            self.won = False
            self.finished = False
            return False
        guess = self.guesses[-1]['guess']
        check_result = self.check(guess)
        if check_result['place'] == 4:
            self.won = True
            self.finished = True
            return True
        if len(self.guesses) >= self.max_guesses:
            self.won = False
            self.finished = True
            return True

    def guess(self, guess):
        result = self.check(guess)
        self.guesses.append({'guess': guess, 'result': result})
        self.finish()
        return self.guesses

    def get_guesses(self):
        return self.guesses

    def get_pattern(self):
        return self.pattern

    def serialize(self):
        data = {
            'pattern': self.pattern,
            'guesses': self.guesses,
        }
        return data

    def deserialize(self, data):
        self.pattern = data['pattern']
        self.guesses = data['guesses']
