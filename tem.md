```
translation_unit : external_decl
                 | translation_unit external_decl
external_decl : funcdef
              | declstmt
statement_list : statement
               | statement statement_list 
statement : assignment_statement 
                  | declstmt
                  | while_statement
                  | funccall_stmt
                  | jump_statement
                  | selection_statement
 typedecl : type cast_expr 
                    | type cast_expr EQUALS expression
arraydecl : type varsymbol LBRACKET INT_CONST RBRACKET EQUALS expression
arraydecl : type varsymbol LBRACKET INT_CONST RBRACKET
funcdecl : storage type methodsymbol LPAREN param_list RPAREN
funcdecl : type methodsymbol LPAREN param_list RPAREN
pointer : TIMES 
                    | pointer TIMES
storage : EXTERN
                    | STATIC     
type : basetype pointer
                 | basetype  
declaration : typedecl 
                        | arraydecl
                        | funcdecl
declstmt : declaration SEMI
compound_statement : LBRACE statement_list RBRACE
while_statement : WHILE LPAREN expression RPAREN compound_statement
if_statement1 : IF LPAREN expression RPAREN compound_statement ELSE compound_statement
if_statement2 : IF LPAREN expression RPAREN compound_statement
selection_statement : if_statement1
                                | if_statement2
break_statement  : BREAK SEMI
continue_statement  : CONTINUE SEMI
jump_statement  : return_statement
                            | continue_statement
                            | break_statement
return_statement : RETURN expression SEMI
return_statement : RETURN SEMI
assignment_statement : assignment_expr SEMI
assignment_expr : cast_expr EQUALS expression
expression : binary_expr
                       | funccall_expr
cast_expr : unary_expr
                      | primary_expr        
 primary_expr : varsymbol
                         | constant     
unary_op : BAND
                     | TIMES
unary_expr : unary_op primary_expr 
binary_expr : binary_expr PLUS binary_expr
                  | binary_expr MINUS binary_expr
                  | binary_expr TIMES binary_expr
                  | binary_expr DIVIDES binary_expr
                  | binary_expr GT binary_expr
                  | binary_expr LT binary_expr
                  | binary_expr LE binary_expr
                  | binary_expr GE binary_expr
                  | binary_expr EQ binary_expr
                  | binary_expr NE binary_expr
                  | binary_expr LAND binary_expr
                  | binary_expr LOR binary_expr
                  | LPAREN binary_expr RPAREN
                  | cast_expr
                  | funccall_expr
param : type varsymbol         
param_list : param
                       | param COMMA param_list
                       | VOID
argument : varsymbol
                     | constant   
argument_list : argument 
                          | argument COMMA argument_list   
funcdef : type methodsymbol LPAREN param_list RPAREN compound_statement
                    | type methodsymbol LPAREN RPAREN compound_statement           funccall_expr : methodsymbol LPAREN argument_list RPAREN
                     | methodsymbol LPAREN RPAREN
funccall_stmt : funccall_expr SEMI
basetype : INT 
                 | CHAR
                 | FLOAT
                 | VOID
methodsymbol : ID         
varsymbol : ID
constant : INT_CONST
constant : CHAR_CONST
constant : FLOAT_CONST
constant : NORMALSTRING
```

shell的BNF
