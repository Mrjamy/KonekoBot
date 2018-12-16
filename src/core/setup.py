import os


class Setup:
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.data = rf'{self.dir_path}/data'

        self.currency = rf'{self.data}/currency.sqlite'
        self.level = rf'{self.data}/currency.sqlite'

    def setup(self):
        self.database()

    def database(self):
        files = [self.currency, self.level]

        for file in files:
            # if not os.path.exists(file):
            #     open(file, 'w').close()
            try:
                file = open(file, 'r')
            except (IOError, FileNotFoundError):
                file = open(file, 'w')
