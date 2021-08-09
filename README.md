 # OFF PLANNER
### Video Demo: https://youtu.be/6s0raqAJ8eI
### Description:

##OFF PLANNER is a simple calendar type web. It’s designated for people doing shift work,their families and friends.
#There are a number of factories in my area and many of my friends or members of their families work over there. This is a shift work including days and nights. Every company has its own work plan system, sometimes more then one. In almost every home in my town there is some kind of paper copy of ‘SHIFT PLAN’ sometimes called ROTA or  Pattern, attached to the fridge in their kitchen. It’s hard to and and check if you’re working on particular day especially if there is more than one shift worker involved.so my app is tool to make their life easier. Thanks to Off Planner I can check if my friends are available for garden party on particular day or If they’re off on the day when their favourite band comes to the town for a gig. Itmaes easier planning of holidays or booking appointment to dentist etc.
    App itself is quite simple. It display calendar of current month with day and night shifts are marked yellow and grey accordingly. Above calendar there is a header describing Company name, shift pattern and currently displaeyd shift. Underneath there is a date(month nd year) and arrows to navigate between months. Underneath of the calendar there are buttons for changing shifts and select list of different companies and their shift plans/systems.
After registering and logging in. Another select menu button appears. This list contain names of persons/friends which can be added to user account to display that person’s shift plan without unnessery navigation. We wont have to remember where and what shift this prticulr person is working.

## technology

#My application was created using Python and its framework flask and SQL bfor backend.
Frontend is coded in HTML JS and CSS. I used Bootstrap and JQuery frameworks.

##SQL database ‘shifts’ consist of following tables:
#Shifts - containing information about company,shift name and shift pattern
#Uzers - containing logon information for users
#Separate table for each user containing default shift plan and information about their friends and their shift plans
##Python application consist of:

#Application.py including routes for all events

##Templates:

#index.html - display calendar
#login.html - display login form
#addperson.html - display add friend form
#registerr.html - display registration form

## Usage

#Navigate through the months using arrow buttons above the calendar.
#Change shifts by pressing buttons under calendar.
#Select company and shift plan using drop down menu.
#Register and login using main top menu.
#After login add friends/person using ADD PERSON button in top menu.
#When logged select shift plan by selecting person from drop down menu under calendar.

##Future development TODO's

#Checking availability of all persons by selected date.

###Author
##Przemysław Stążka
#primeau.stone@gmail.com

## License
[MIT](https://choosealicense.com/licenses/mit/)
