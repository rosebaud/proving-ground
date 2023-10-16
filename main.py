from collections import deque
import random

class Base:

    def is_non_terminal(self, symbol):
        return True if symbol[0] == "$" else False
    
    def identify(self, symbol):
        return Non_Terminal(symbol) if self.is_non_terminal(symbol) else Terminal(symbol)

    def parse(self, axiom):
        return [self.identify(symbol) for symbol in axiom.split()]


class Terminal:
    is_terminal = True
    string = ""
    def __init__(self, symbol):
        self.symbol = symbol
        self.string = symbol

    def __repr__(self):
        return "T:{}".format(self.symbol)        

class Non_Terminal(Base):
    is_terminal = False
    def __init__(self, symbol):
        # super().__init__(self)
        self.symbol = symbol
        self.stack = deque()
        self.stack.append(self.symbol)
        self.expansion = []

    def __repr__(self):
        return "NT:{}".format(self.symbol)

    def expand(self, lex):
        #print(lex.keys())
        resp = []
        while self.stack:
            #print("Stack:", self.stack)
            current = self.stack.pop()
            exp = random.choice(lex[current])
            print("Expanded {} -> {}".format(current, exp))
            # Add non-terminal symbols to stack
            self.add_non_terminals(exp)

        return " ".join(self.expansion)

    def add_non_terminals(self, symbols):
        for sym in symbols:
            if not sym.is_terminal:
                #print("Expanding:", sym)
                self.stack.append(sym.symbol)
            else:
                #print("Saving", sym)
                self.expansion.insert(0, sym.symbol)

class Grammar(Base):
    """A simple context-free grammar parser"""

    def __init__(self):

        self.lexicon = {
            "$animal": ["$color cat", "$color dog", "$color finch"],
            "$color": ["red", "blue", "green"],
            "$verbs": ["dances", "snoozes"]
        }

        self.symbol_lex = {}
        self.prepare_lexicon()

    def prepare_lexicon(self):
        for key in self.lexicon.keys():
            data = self.lexicon[key]
            self.symbol_lex[key] = [self.parse(d) for d in data]

    def solve(self, axiom):
        response = []
        symbols = self.parse(axiom)
        for sym in symbols:
            print("-"*80)
            print("Solving:", sym)
            if not sym.is_terminal:
                exp = sym.expand(self.symbol_lex)
                response.append(exp)
            else:
                response.append(sym.string)
        resp_string = " ".join(response)
        print(resp_string)



if __name__ == "__main__":
    # Start with axiom
    gram = Grammar()

    axiom = "The $animal $verbs"
    gram.solve(axiom)
    # Get random non-terminal from axiom
    # $animal | $verbs

    # Expand the non-terminal and stash the result in a stack
    # exp = [$color cat, $color dog] $animal
    # exp = $color cat
    # stack = exp

    pass
