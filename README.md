# COMP3297-SSEFinder
- COMP3297 Group F Project

## Main
App Link (Heroku) : https://frozen-waters-91223.herokuapp.com/CovidDataPortal/


## Instructions

- Update Heroku
	- No need manual update, I have set Heroku auto update with this res, after changing things here, wait a while and reload the heroku page to see changes.

- Setting up (git)
	- Login github in local terminal
	- Add this res
		- git remote add github https://github.com/Felix-Ku/COMP3297-SSEFinder.git
	- Pull all files into your local directory

- Everytime update (Method 1: using Git after setting up)
	- (If new files added) git add --all
	- git commit -m "COMMIT NAME"
	- git push github master

- Everytime update (Method 2: Directly editing files on Github)
	- Just edit the files and commit changes

- To add new pages:
	- Add new template pages inside \templates\
	- Create function for the new page into \Portal\views.py
	- Add new function and page info into \Portal\urls.py
	- Create links in base.html
