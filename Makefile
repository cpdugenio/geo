.PHONY: learned

SECRET_FILE     := .SECRET
SECRET 			:=$(file < $(SECRET_FILE))

all: anki learned

anki: 
	env NOTION_TOKEN=$(SECRET) python -m geo anki

learned: 
	env NOTION_TOKEN=$(SECRET) python -m geo learned
