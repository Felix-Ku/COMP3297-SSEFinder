# COMP3297-SSEFinder
- COMP3297 Group F Project

## Main
App Link (Heroku) : https://frozen-waters-91223.herokuapp.com/CovidDataPortal/

## Limitations

- Clients should input dates in the format of "dd/mm/YYYY".
- Client should provide its login details to login the system before using

## Coding instructions

- Update Heroku
	- No need manual update, I have set Heroku auto update with this res, after changing things here using Git, wait a while and reload the heroku page to see changes.

- Setting up (git)
	- Login github in local terminal
	- Add this res
		- git remote add github https://github.com/Felix-Ku/COMP3297-SSEFinder.git
	- Pull all files into your local directory
		- git pull github master

- Everytime update (Method 1: using Git after setting up)
	- (If new files added) git add --all
	- git commit -m "COMMIT NAME"
	- git push github master

- Everytime update (Method 2: Directly editing files on Github)
	- Just edit the files and commit changes

- *Update Models
	- Comment codes in settings.py
	- Uncomment local codes in settings.py
	- Run : python manage.py makemigrations CovidDataPortal
	- Run : python manage.py migrate
	- git add --all
	- git commit
	- push
	- heroku run python mamange.py makemigrations CovidDataPortal
	- heroku run python manage.py migrate CovidDataPortal

- Check error logs
	- heroku logs tail--

- To add new pages:
	- Add new template pages inside \templates\
	- Create function for the new page into \Portal\views.py
	- Add new function and page info into \Portal\urls.py
	- Create links in base.html

## Extra
- CMD
- heroku  login
- (If new files added) git add --all
- git commit -m "COMMIT NAME"
- git push github master / git push heroku master

## Author of readme
- Felix Ku Sze Hung
