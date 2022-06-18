.PHONY: anki learned unlearned

SECRET_FILE     := .SECRET
SECRET 			:=$(file < $(SECRET_FILE))

all: anki learned unlearned

anki: 
	env NOTION_TOKEN=$(SECRET) python -m geo anki

learned: 
	env NOTION_TOKEN=$(SECRET) python -m geo learned

unlearned: 
	env NOTION_TOKEN=$(SECRET) python -m geo unlearned
