%{
#include<stdio.h>
#include<stdlib.h>
#include "2020244_Parser.tab.h" // Include the parser header file for token definitions
extern int yylval; // External declaration of yylval provided by the parser
%}

%%

[0-9]+            { yylval = atoi(yytext); return NUMBER; } // Match and convert numbers
[-+*/%^()]        { return yytext[0]; } // Return arithmetic operators and parentheses
[ \t\n]           ; // Ignore whitespace and newline characters

.                 { // Handle invalid characters
                    printf("Invalid character: %c\n", yytext[0]);
                    exit(1);
                  }

%%

int yywrap() {
    return 1;
}
