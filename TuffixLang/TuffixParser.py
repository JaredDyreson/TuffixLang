from rply import ParserGenerator
from TuffixLang.TuffixAST import *

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

        @self.pg.production('expression : ADD TARGET')
        def install(p):
            target = p[1].getstr().strip()
            return Install(target)

        @self.pg.production('expression : REMOVE TARGET')
        def remove(p):
            target = p[1].getstr().strip()
            return Remove(target)

        @self.pg.production('expression : REINSTALL TARGET')
        def reinstall(p):
            target = p[1].getstr().strip()
            return Reinstall(target)

        @self.pg.production('expression : REINSTALL GLOB')
        def reinstall_complete(p):
            return Reinstall("*")

        @self.pg.production('expression : DESCRIBE TARGET')
        def describe(p):
            target = p[1].getstr().strip()
            return Describe(target)

        @self.pg.production('expression : STATUS')
        def host_information(p):
            return Status(p)

        @self.pg.production('expression : COMMENT')
        def ignore_comment(p):
            return Ignore(p)

        @self.pg.production('expression : ENV')
        def print_env(p):
            environment = p[0].getstr().strip().split()[1]
            return PrintEnv(environment)

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
        @self.pg.production('expression : HELP')
        def help_message(p):
            return Help(p)

        @self.pg.error
        def error_handle(token):
            raise Exception(token)

    def get_parser(self):
        return self.pg.build()

