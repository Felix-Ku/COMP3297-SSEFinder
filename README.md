# SSEFinder-3297
COMP3297 Group F Project

## To-Do
1. Set up git resp
2. Register Jira accounts
3. Set up Google doc / Use Slack
4. Schedule meeting with Cristy on Moodle
5. Digest project requirements
6. Create working schedule (on Jira?)
7. Endless coding

## Our links

- Jira page：
    - http://

- Google drive：
    - https://drive.google.com/drive/folders/1hlnsnbRXQHm_aqzXlIS2DP5DncT7ecPf?usp=sharing

- Slack page：
    - http://


## Project details

### Background of user requirement
Superspreading Event (SSE) refers to situations while the people infected with Covid spread the virus to many more than 3 others and causes subsequent infections to other individuals. Such events normally take place in small and crowded places where a group of people gathered for social activities. 

Currently, the staff at Centre for Health Protection (CHP) records the data one by one in Excel files and identify signs of SSEs manully, they now want a automated application to make the tedious process automated.

### Environments
- Heroku
- Django
- PostgreSQL

### Function of application to be implemented
- (Through admin page?) Allow input and store of data by staffs
- Allow staff to search for cases using case number
- Allow staff to select a case, and allow staff to then input detail information of attendance at social events for it.
    - Venue name (a restaurant name, for example)
    - Venue location
    - (Auto retrive by application) Address of the venue location (if available in the Geodata dataset)
    - (Auto retrive by application) HK1980 Grid Coordinates of the venue location 
    - Date of the event
    - Brief description of the event
- Automatically get the location address and its HK1980 grid coordinates according to new venue of event input by staff
- Identify possible SSEs and store them with time specified
- Allow staff to select date range to view the possible SSE cases
- Allow access only by epidemiologists
- (Through admin page?) Allocate username and password for aforesaid personnel
- (Through admin page?) Main the login and personal information of epidemiologists
    - username,
    - password,
    - CHP staff number (6-digit string),
    - first name,
    - last name,
    - email address.

### Data input by user
- Covid case
    - Case Number (unique)
    - Person name
    - Identity Document Number (unique)
    - Date of Birth
    - Date of onset of symptoms
    - Date of confirmation of infection by testing

- Event details
    - Venue name (a restaurant name, for example)
    - Venue location
    - (Allow to leave blank for automatic retrieval?) Address of the venue location (if available in the Geodata dataset)
    - (Allow to leave blank for automatic retrieval?) HK1980 Grid Coordinates of the venue location
    - Date of the event
    - Brief description of the event

### Api interfaces

- Location search using GeoData
    - https://geodata.gov.hk/gs/locationSearchAPI


### Classifying SSEs
· SSE: An SSE is an event which results in more than 6 new infections (MIT data). Until it is known
for certain that sufficient cases were actually infected during the event, the event can only be
classified as a potential SSE.
· Infector: A person infected with the coronavirus can spread it to others starting 3 days before the
onset of symptoms (WHO data). Often the person is unaware they were infected until they are tested
after developing symptoms. Thus, the infectious period for a case is from 3 days before onset of
symptoms, through until the person isolates after testing positive. If the person attends an event
during their infectious period, then they are classified as a possible infector for that event. There
may be several possible infectors at any event.
· Infected: The incubation period of the disease can be as long as 14 days or as short as 2 days
(WHO data). A person who develops sympto

### General assumptions

- Location Search will always provide exactly one match unless it fails with a non-200 status code (this
is to simplify your task; your application will be evaluated only with venue locations for which there
is a single match);
- when an infection is confirmed, that person is immediately isolated and will not attend any subsequent
events until no longer infectious;
- a person will never become reinfected after recovering from COVID-19. Thus, a person cannot be the
subject of more than one case;
- there will be no cases of asymptomatic infection;
- epidemiologists act in a disciplined way. For instance, they will never create duplicate attendance
records for the same case;
- that when a user updates data, there is no need to reflect that change immediately to other users who,
for example, may be viewing the data.

