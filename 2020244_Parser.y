%{
#include<stdio.h>
#include<stdlib.h>
#include<math.h>
%}

%token NUMBER // Define the token NUMBER

%%

ArithmeticExpression: Expression { printf("\nResult = %d\n\n", $1); }; // Define the top-level rule for arithmetic expressions

Expression: Term // Define the expression rule
          | Expression '+' Term { $$ = $1 + $3; } // Addition operation
          | Expression '-' Term { $$ = $1 - $3; } // Subtraction operation
          ;

Term: Factor // Define the term rule
    | Term '*' Factor { $$ = $1 * $3; } // Multiplication operation
    | Term '/' Factor { 
                        if ($3 != 0)
                            $$ = $1 / $3; 
                        else {
                            yyerror("Division by zero");
                        }
                      } // Division operation
    | Term '%' Factor { $$ = $1 % $3; } // Modulus operation
    ;

Factor: Primary // Define the factor rule
      | Factor '^' Primary { $$ = pow($1, $3); } // Exponentiation operation
      ;

//Precendece for the () operator
Primary: NUMBER // Define the primary rule
       | '(' Expression ')' { $$ = $2; } // Parenthesized expression
       ;

%%

void yyerror(const char *s) {
    printf("Error: %s\n", s); // Print error message
    exit(1); // Exit with failure status
}

int main() {
    printf("\nArithmetic expression: ");
    yyparse(); // Parse the input arithmetic expression
    return 0; // Return success status
}
