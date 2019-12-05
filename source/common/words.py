import random


class Manager:
    def __init__(self):
        langs = (Dragish(),
                 Dwarish(),
                 Elvish(),
                 Gobish(),
                 Himan(),
                 Loman()
                 )

        self.langs = {}
        for lang in langs:
            self.langs[lang.lang_name] = lang

    def get_word(self, lang):
        return self.langs[lang].get_word()

    def get_names(self, lang):
        return self.langs[lang].get_names()


class Language:
    def __init__(self, lang_name):
        self.lang_name = lang_name

    def get_word(self):
        return

    def get_name(self):
        return


class Dragish(Language):
    def __init__(self):
        Language.__init__(self, 'Dragish')

    def get_word(self):
        return 'Dreth'

    def get_name(self):
        return 'Dorum', 'Wind'


class Dwarish(Language):
    def __init__(self):
        Language.__init__(self, 'Dwarish')

    def get_word(self):
        return 'Horsh'

    def get_name(self):
        return 'Kellum', 'Brock'


class Elvish(Language):
    def __init__(self):
        Language.__init__(self, 'Elvish')

    def get_word(self):
        return 'Hellen'

    def get_name(self):
        return 'Olyn', 'Maice'


class Gobish(Language):
    def __init__(self):
        Language.__init__(self, 'Gobish')

        self.vowel_start = ('a', 'o', 'u')
        self.vowel = ('a', 'e', 'i', 'o', 'u')
        self.alpha = ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'x', 'z')

    def get_word(self):
        word = ''
        syls = random.randint(2, 5)
        for syl in range(syls):
            r = random.randint(1, 6)
            if r <= 2:
                v = random.randint(0, len(self.vowel_start) - 1)
                c = random.randint(0, len(self.alpha) - 1)
                word = word + self.vowel_start[v] + self.alpha[c]
            elif r <= 5:
                v = random.randint(0, len(self.alpha) - 1)
                c = random.randint(0, len(self.vowel) - 1)
                word = word + self.alpha[v] + self.vowel[c]
            elif r == 6:
                v = random.randint(0, len(self.alpha) - 1)
                c = random.randint(0, len(self.vowel_start) - 1)
                s = random.randint(0, len(self.vowel_start) - 1)
                word = word + self.alpha[v] + self.vowel_start[c] + self.vowel_start[s]

        r = random.randint(1, 10)
        if r <= 6:
            word = word
        elif r <= 8:
            word = word + 'ish'
        elif r == 9:
            word = word + 'esh'
        elif r == 10:
            word = word + 'oth'

        return word

    def get_names(self):
        self_name = self.get_word()

        r = random.randint(1, 8)
        v = random.randint(1, 10)

        if r == 0:
            if v == 0:
                kin_name = 'Goborn'
            elif v <= 2:
                kin_name = 'Gobor'
            else:
                kin_name = 'Gobbor'
        else:
            if v == 0:
                kin_name = 'Orcborn'
            elif v <= 2:
                kin_name = 'Orborn'
            elif v <= 4:
                kin_name = 'Orbor'
            else:
                kin_name = 'Orcbor'

        return self_name, kin_name


class Himan(Language):
    def __init__(self):
        Language.__init__(self, 'Himan')

    def get_word(self):
        return 'Hello'

    def get_name(self):
        return 'Kecin', 'Paeity'


class Loman(Language):
    def __init__(self):
        Language.__init__(self, 'Loman')

    def get_word(self):
        return 'Hi'

    def get_name(self):
        return 'Kayish', 'Paeman'
