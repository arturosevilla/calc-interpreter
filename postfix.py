#!/usr/bin/env python
from postfix.compiler import Parser, Lexer

def interpret():
    try:
        expression = raw_input('> ')
    except EOFError:
        return False
    try:
        print Parser(Lexer(expression)).parse()
    except Exception, e:
        print str(e)
    return True

if __name__ == '__main__':
    should_continue = True
    while should_continue:
        should_continue = interpret()
