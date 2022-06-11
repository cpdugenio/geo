.PHONY: learned

SECRET_FILE     := .SECRET
SECRET 			:=$(file < $(SECRET_FILE))

learned: 
	env NOTION_TOKEN=$(SECRET) python -m geo learned
