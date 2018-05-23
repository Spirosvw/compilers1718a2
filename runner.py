import plex

class ParseError(Exception):
	pass


class RunError(Exception):
  pass

class MyParser():
        def __init__(self):
            self.st = {}

        def create_scanner (self, fp):
            letter = plex.Range("azAZ")
            digit = plex.Range("09")
            name = letter + plex.Rep(letter | digit)
            space = plex.Rep1(plex.Any(" \n\t"))
            keyword = plex.Str("print")


            operator_and_or=plex.Str("and","or")
            operator_not=plex.Str("not")
            operator_equal=plex.Str("=")
            operator_parenth=plex.Str("(",")")
            operator_false=plex.NoCase(plex.Str('0','f','false'))#den exei shmasia an einai kefalaia h mikra
            operator_true = plex.NoCase(plex.Str('1', 't', 'true'))  # den exei shmasia an einai kefalaia h mikra


            lexicon = plex.Lexicon([
                (keyword, plex.TEXT),
                (operator_and_or,plex.TEXT),
                (operator_not,plex.TEXT),
                (operator_false,"FALSE"),
                (operator_true,"TRUE"),
                (name, "IDENTIFIER"),
                (space, plex.IGNORE),
                (operator_parenth,plex.TEXT),
                (operator_equal,plex.TEXT)
            ])


            self.scanner = plex.Scanner(lexicon, fp)
            self.la, self.val = self.next_token()


        def parse(self, fp):
            self.create_scanner(fp)
            self.stmt_list()


        def next_token(self):
            return self.scanner.read()


        def stmt_list(self):
            if self.la == "IDENTIFIER" or self.la=="print":
                self.stmt()
                self.stmt_list()
            elif self.la is None:
                raise ParseError("Expecting", self.la)


        def stmt(self):
            if self.la == "IDENTIFIER":
                vr=self.val
                self.match("IDENTIFIER")
                self.match("=")
                self.st[vr]=self.expr()
            elif self.la == "print":
                self.match("print")
                print(self.expr())
            else:
                raise ParseError("Invalid command(Id or print command expected)")


        def expr(self):
                if self.la=="(" or self.la=="IDENTIFIER" or self.la=="FALSE" or self.la=="TRUE":
                    a=self.term()
                    b=self.term_tail()
                if b is None:
                    return a
                if b[0]=="or":
                    return self.operator_or(a,b[1])
                else:
                    raise ParseError("Expected",self.la)


        def term_tail(self):
            if self.la == "and" or self.la == "or":
                op = self.operator_and_or()
                a = self.term()
                b = self.term_tail()
                if b is None:
                    return op, a
                if b[0] == "or":
                    return op, self.operator_or(a, b[1])
            elif self.la == "IDENTIFIER" or self.la == "print" or self.la == ")" or self.la == None:
                return
            else:
                raise ParseError("Expected keyword AND or OR")


        def term(self):
                if self.la=="(" or self.la=="IDENTIFIER" or self.la=="FALSE" or self.la=="TRUE" or self.la=="not":
                    f = self.factor()
                    ft = self.factor_tail()
                    if ft is None:
                        return f
                    if ft[0] == "and":
                        return self.operator_and(f, ft[1])
                else:
                    raise ParseError("Expected id ,boolean operator or 'not' operator")


        def factor_tail(self):
                if self.la=="not":
                    self.operator_not()
                    self.factor()
                    self.factor_tail()
                    if ft is None:
                        return op,ft
                    if ft[0]=="*":
                        return op,f*ft[1]
                elif self.la=="and" or self.la=="or" or self.la=="IDENTIFIER" or self.la=="print" or self.la==None or self.la== ")":
                    return
                else:
                    raise ParseError("Expected 'not' operator")


        def factor(self):
            if self.la == "and":
                op = self.operator_and_or()
                f = self.factor()
                ft = self.factor_tail()
                if ft is None:
                    return op, f
                if ft[0] == "and":
                    return op, self.operator_and(f, ft[1])
            elif self.la == "IDENTIFIER":
                varname = self.val
                self.match(self.la)
                if varname in self.st:
                    if not_op == "not":
                        return self.operator_not(self.st[varname])
                    else:
                        return self.st[varname]


                raise RunError("Unitialized variable: ", varname)

            elif self.la=="true" or self.la=="false":
                token = self.la
                self.match(token)
                if not_op == "not":
                    return self.operator_not(token)
                else:
                    return token
            else:
                raise ParseError("Excpected: id, (expr), values")

        def match(self, token):
            if self.la == token:
                self.la, self.val = self.next_token()
            else:
                raise ParseError("Expected ", self.la)



        def operator_and_or(self):
            if self.la== "and":
                self.match('and')
            elif self.la=="or":
                self.match('or')
            else:
                raise ParseError("Expected AND or OR")


        def oper_not(self):
            if self.la == "not":
                self.match('not')
            else:
                raise  ParseError("Expected NOT operator")

        def operator_or(self,a,b):
            if a == "False" and b == "False":
                return "False"
            else:
                return "True"


        def operator_and(self,a,b):
            if a == "True" and b == "True":
                return "True"
            else:
                return "False"

        def operator_not(self,a,b):
            if a == "False":
                return "True"
            else:
                return "False"


p = MyParser()
fp = open("text.txt", "r")
try:
    p.parse(fp)
except ParseError as perr:
    print(perr)

fp.close()






