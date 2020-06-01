from rply import ParserGenerator
from TuffixAST import *

class Parser():
    def __init__(self, tokens: dict):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            list(tokens.keys())
        )

    def parse(self):
        @self.pg.production('expression : TARGET')
        def epxression_target(p):
            return Target(str(p[0].getstr()))

        @self.pg.production('expression : ADD')
        def install(p):
            target = str(p[0].getstr()).split()[1]
            return Install(target)

        @self.pg.production('expression : REMOVE')
        def remove(p):
            target = str(p[0].getstr()).split()[1]
            return Remove(target)

        @self.pg.production('expression : DESCRIBE_TARGET')
        def describe(p):
            target = str(p[0].getstr()).split()[1]
            return Describe(target)

        @self.pg.production('expression : STATUS')
        def host_information(p):
            return Status(p)

        @self.pg.production('expression : COMMENT')
        def ignore_comment(p):
            return Ignore(p)

        @self.pg.production('expression : INIT')
        def initialize_tuffix(p):
            return Initialize(p)

        @self.pg.production('expression : LIST_INSTALLED')
        def list_installed(p):
            return ListInstalled(p)

        @self.pg.production('expression : LIST_AVAILABLE')
        def list_availble(p):
            return ListAvailable(p)

        @self.pg.production('expression : REKEY')
        def start_rekey(p):
            return Rekey(p)

        @self.pg.error
        def error_handle(token):
            raise Exception(token)

    def get_parser(self):
        return self.pg.build()

