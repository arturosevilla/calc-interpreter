
class UnknownToken(Exception):
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return self.message


class UnexpectedToken(Exception):
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return self.message


class Token(object):
    def __init__(self, type_, lexeme=None):
        self.type_ = type_
        self.lexeme = lexeme


class TokenType(object):
    NUM = 0
    OP = 1
    OPEN_PARENS = 2
    CLOSING_PARENS = 3


class Lexer(object):

    def __init__(self, program):
        self.program = program.strip()
        self.reset()

    def reset(self):
        self.current = 0
        self.finished = False

    def is_number(self, val):
        if val is None:
            return False
        return '0' <= val <= '9'

    def next(self):
        if self.current < len(self.program):
            next_ = self.program[self.current]
            self.current += 1
            return next_
        else:
            self.finished = True
            return None

    def unread(self):
        if self.current >= 0 and not self.finished:
            self.current -= 1


    def get_next_token(self):
        look_ahead = self.next()
        while look_ahead in [' ', '\t', '\n']:
            look_ahead = self.next()
        if look_ahead == '(':
            return Token(TokenType.OPEN_PARENS)
        if look_ahead == ')':
            return Token(TokenType.CLOSING_PARENS)

        if self.is_number(look_ahead):
            number = int(look_ahead)
            look_ahead = self.next()
            while self.is_number(look_ahead):
                number *= 10
                number += int(look_ahead)
                look_ahead = self.next()
            self.unread()
            return Token(TokenType.NUM, number)
        elif look_ahead in ['+', '-', '*']:
            return Token(TokenType.OP, look_ahead)
        elif look_ahead is None:
            return None
        else:
            raise UnknownToken('Unknow token ' + look_ahead)


# term -> factor factor_rest
# factor -> num | (expr)
# factor_rest-> * term | / term
# factor_rest -> epsilon
# *expr -> term term_rest
# term_rest -> + term | - term
# term_rest -> epsilon
# num -> [0-9]+



class Parser(object):

    def __init__(self, lexer):
        self.lexer = lexer
        self._fallback = None

    def fallback(self, token):
        self._fallback = token

    def match(self, types, allow_empty=False):
        if not isinstance(types, list):
            types = [types]
        if self._fallback is not None:
            token = self._fallback
            self._fallback = None
        else:
            token = self.lexer.get_next_token()
        if token is None and allow_empty:
            return None
        elif token is None or token.type_ not in types:
            if token is None:
                token_type = '(empty)'
            else:
                token_type = token.type_
            self.fallback(token)
            raise UnexpectedToken(token_type)
        return token
    
    def parse(self):
        return self.expr()

    def expr(self):
        token = self.term()
        return self.term_rest(token)

    def factor(self):
        token = self.match([TokenType.NUM, TokenType.OPEN_PARENS])
        if token.type_ == TokenType.OPEN_PARENS:
            translation = self.expr()
            self.match(TokenType.CLOSING_PARENS)
            return translation
        return str(token.lexeme)

    def factor_rest(self, expression):
        try:
            token = self.match(TokenType.OP, True)
        except UnexpectedToken:
            token = None

        if token is None:
            return expression
        if token.lexeme == '*':
            expression += ' ' + self.term()
            return expression + ' *'
        elif token.lexeme == '/':
            expression += ' ' + self.term()
            return expression + ' /'
        else:
            self.fallback(token)
            return expression

    def term(self):
        token = self.factor()
        return self.factor_rest(token)

    def term_rest(self, expression):
        token = self.match(TokenType.OP, True)
        if token is None:
            return expression
        if token.lexeme == '+':
            expression += ' ' + self.term()
            return expression + ' +'
        elif token.lexeme == '-':
            expression += ' ' + self.term()
            return expression + ' -'
        else:
            raise ValueError('This should not happen!')


    def reset(self):
        self.lexer.reset()

