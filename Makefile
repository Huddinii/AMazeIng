all:
	@+make test
	@make install

install:
	python3 -m pip install

run:
	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb

clean:
	make clean -C

lint:
	flake8 .
	mypy . --warn-return-any--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs--check-untyped-defs

lint-strict:
	flake8 .
	mypy --strict .

.PHONY: all install run debug clean