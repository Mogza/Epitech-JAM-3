##
## EPITECH PROJECT, 2024
## Makefile
## File description:
## Makefile
##

SRC= 	src/main.cpp

NAME= jam

OBJ= $(SRC:.cpp=.o)

CXXFLAGS = -Werror -Wextra -Wall

.PHONY = all, clean, fclean, re

all: $(NAME)

$(NAME):	$(OBJ)
	g++ -o $(NAME) $(OBJ) $(CXXFLAGS)

clean:
		rm -f $(OBJ)

fclean: clean
		rm -f $(NAME)

re:     fclean all
