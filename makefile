all:
	make clean-up
	make build

clean-up:
	rm preproccesed/*modified.jpg

build:
	python3 ocr.py 

