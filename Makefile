NAME := a_maze_ing.py config.txt

.PHONY: all install run debug clean lint lint-strict

all: install lint lint-strict run

install:
	python3 -m pip install

run:
	python3 $(NAME)

debug:
	python3 -m pdb $(NAME)

clean:
	rm -rf __pycache__

lint:
	flake8 .
	mypy . --warn-return-any--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs--check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
