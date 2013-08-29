
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
    def __init__(self, type_, lexeme):
        self.type_ = type_
        self.lexeme = lexeme


class TokenType(object):
    NUM = 0
    OP = 1


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
        if self.is_number(look_ahead):
            number = int(look_ahead)
            look_ahead = self.next()
            while self.is_number(look_ahead):
                number *= 10 + int(look_ahead)
                look_ahead = self.next()
            self.unread()
            return Token(TokenType.NUM, number)
        elif look_ahead in ['+', '-', '*']:
            return Token(TokenType.OP, look_ahead)
        elif look_ahead is None:
            return None
        else:
            raise UnknownToken('Unknow token ' + look_ahead)


class Expression(object):
    def eval(self):
        raise NotImplementedError()


class BinaryExpression(Expression):
    
    def __init__(self, left, right):
        self.left = left
        self.right = right


class SumOperation(BinaryExpression):

    def __init__(self, left, right):
        super(SumOperation, self).__init__(
            left,
            right
        )

    def eval(self):
        return self.left.eval() + self.right.eval()

class DifferenceOperation(BinaryExpression):

    def __init__(self, left, right):
        super(DifferenceOperation, self).__init__(
            left,
            right
        )

    def eval(self):
        return self.left.eval() - self.right.eval()


class ProductOperation(BinaryExpression):

    def __init__(self, left, right):
        super(ProductOperation, self).__init__(
            left,
            right
        )

    def eval(self):
        return self.left.eval() * self.right.eval()



class ConstExpression(Expression):

    def __init__(self, number):
        self.number = number

    def eval(self):
        return self.number

# expr -> num rest
# rest -> + expr | - expr
# rest -> epsilon
# num -> [0-9]+



class Parser(object):

    def __init__(self, lexer):
        self.lexer = lexer


    def match(self, type_, allow_empty=False):
        token = self.lexer.get_next_token()
        if token is None and allow_empty:
            return None
        elif token is None or token.type_ != type_:
            if token is None:
                token_type = '(empty)'
            else:
                token_type = token.type_
            raise UnexpectedToken(token_type)
        return token
    
    def parse(self):
        return self.expr()

    def expr(self):
        token = self.match(TokenType.NUM)
        return self.rest(token)

    def rest(self, num):
        token = self.match(TokenType.OP, True)
        if token is None:
            return ConstExpression(num.lexeme)
        if token.lexeme == '+':
            return SumOperation(
                ConstExpression(num.lexeme),
                self.expr()
            )
        elif token.lexeme == '-':
            return DifferenceOperation(
                ConstExpression(num.lexeme),
                self.expr()
            )

        else:
            raise ValueError('This should not happen!')


    def reset(self):
        self.lexer.reset()

    def eval(self):
        ast = self.parse()
        return ast.eval()
        
