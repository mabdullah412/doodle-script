## Grammer

## Context Free Grammar

line            → expression exit_command

line            → line expression exit_command

line            → exit_command

line            → line exit_command

line            → UserIn VAR '=' expression exit_command

line            → Print expression exit_command

***

expression      → term

expression      → term '+' expression

expression      → term '-' expression

expression      → term UserIn

expression      → VAR

***

term            → factor

term            → factor '*' term

term            → factor '/' term

term            → factor UserIn

term            → VAR

***

factor          → primary

factor          → primary '^' factor

factor          → primary UserIn

factor          → VAR

***

primary         → number

primary         → '(' expression ')'

***

exit_command    → EXIT