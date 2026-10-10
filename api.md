# Server API
### data type
Data | Expected Value | Type
:---             |:---            |---
Date & Time      | Unix timestamp | Number
Student ID (sid) |                | String

### auth
- Authorization header
- session cookie(s)

### method
- GET read data, use url query
- POST update, add, edit data. response response with process status
	-  **should it also return the edited data?**
- DELETE mark data as deleted



## path(s)
### /attendant
- GET: all students attendant
- POST: update single or mulitple student

### /assignment
- GET: all students, assignment and score
	- can be **query** by **sid** GET parameter
- POST: update or add student(s) assignment score
- DELETE: parameter **assignment_id**


### /calendar/event
- GET: return events (everything)
	- parameters
		- from
		- to

- POST: add event
	- body
		- title
		- date
		- detail
- DELETE: delete event

### /calendar/current_month
- GET: return current month events
### /calendar/notification
- GET: weekly (next 7 days) events

### /students
- GET: returns
	- sid
	- firstname
	- lastname
	- sex
	- prefix?
- POST: add and update records
	- body
		- sid(update)
		- firstname
		- lastname
		- sex
		- prefix
- DELETE: delete from db

###  /teacher
- GET:
	- returns
		- id
		- firstname
		- lastname
		- sex
		- prefix?
		- other data
	- parameter
		 - id
- POST: update/add data
	- body
		- tid (update)
		- firstname
		- lastname
		- sex
		- prefix
		- other data

### /activity
- GET
	- query by **id**
	- if not, return (id, title)
- POST
	- add new activity
	- body
		- title
		- description
		- image
- DELETE: parameter **id**

### /file
- GET
	- no parameter (id, author_id, title, category, target)
	- with parameter
		- return the queried result (id, author_id, title, category, target)
- POST: add/edit data
	-  body
		- id(edit)
		- title
		- category
		- target
		- file
		- link
	- edit
		- url param `id`
		- body as normal add
- DELETE


### /search/{search_type}
- GET
	- search_type are { files, students, assignment}
	- file parameter
		- query (keyword)
		- tag (tag separated by comma)
		- uploader
		- filetype {link, text, image}
	- students parameter
		- firstname_or_lastname
		- firstname
		- lastname
		- student id
	- assignment parameter
		- query (keyword)
		- class/room
