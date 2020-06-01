from rply import LexerGenerator

class Lexer():
    def __init__(self, token_map: dict):
        self.lexer = LexerGenerator()
        self.token_map = token_map

    def _add_tokens(self):
        for token_name, token in self.token_map.items():
          self.lexer.add(token_name, token)
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
