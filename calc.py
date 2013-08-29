#!/usr/bin/env python

from compiler import Lexer, Parser

def interpret():
    try:
        expression = raw_input('> ')
    except EOFError:
        print '\n'
        return False
    try:
        print Parser(Lexer(expression)).eval()
    except Exception, e:
        print str(e)
    return True
    

if __name__ == '__main__':
    should_continue = True
    while should_continue:
        should_continue = interpret()

