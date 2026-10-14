# Server API
### data type
Data        | Expected Value      | Type
:---        |:---                 |---
Date & Time | YYYY-MM-DD HH:MM:SS | String
Student ID  |                     | String

### auth
- session cookie(s)
	- session_id
	- teacher_id

### method
- GET read data, use url query
- POST update, add, edit data. response response with process status
	- **should it also return the edited data?**
- DELETE mark data as deleted



## path(s)
### /attendant
- GET: all students attendant
- POST: update single or mulitple student


### `/student/list` DONE
- GET: list students data added by requested teacher
- response body
```json
[
	{
		"student_id": string,
		"prefix": string,
		"firstname": string,
		"lastname": string,
		"sex": string
	},
	...
]
```

### `/student/add` DONE
- POST: add student data
- request/response body
```json
{
	"student_id": string (require),
	"firstname": string (require),
	"lastname": string (require),
	"prefix": string,
	"sex": string
}
```

### `/student/edit` DONE
- POST: edit student data by `student_id` parameter
- request body
```json
{
	"firstname": string,
	"lastname": string,
	"prefix": string,
	"sex": string
}
```
- response body (see `/student/add`)

### `/student/remove` DONE
- POST: remove student data by `student_id` parameter

### `/assignment/info` DONE
- GET: assignment info of `assignment_id` parameter
- response body
```json
{
	"id": number,
	"name": string,
	"subject": string,
	"topic": string,
	"class": number,
	"room": number,
	"max_score": number
	"due": "YYYY-MM-DD HH:MM:SS" or null (no deadline)
	"create_at": "YYYY-MM-DD HH:MM:SS"
}
```

### `/assignment/list` DONE
- GET: list of assignment created by teacher whom request it.
- response body
```json
[
	{
		"id": number,
		"name": string,
		"subject": string,
		"topic": string,
		"class": number,
		"room": number,
		"max_score": number
		"due": "YYYY-MM-DD HH:MM:SS" or null (no deadline)
		"create_at": "YYYY-MM-DD HH:MM:SS"
	},
	...
]
```

### `/assignment/add` DONE
- POST: add new assignment, returns added assignment object
- request body
```json
{
	"name": string (require),
	"subject": string (require),
	"topic": string (require),
	"class": number (1-12) (require),
	"room": number (default 1),
	"max_score": (default 0)
}
```
- response body (see `/assignment/info`)

### `/assignment/edit` DONE
- POST: edit assignment pointed by `assignment_id` parameter, returns added assignment object
- request body
```json
{
	"name": string (optional),
	"subject": string (optional),
	"topic": string (optional),
	"class": number (optional),
	"room": number (optional),
	"max_score": number (optional)
	"due": "YYYY-MM-DD HH:MM:SS" (optional)
}
```
- response body (see `/assignment/info`)


### `/score` DONE
- parameter: `assigment_id`
- GET: returns assignment information and it's score
	- resonse body
```json
{
	"assignment_info": {
		"id": number,
		"name": string,
		"topic": string,
		"subject": string,
		"due": string,
		"max_score": number
		"create_at": string
	},
	"score": [
		{
			"student_id": string,
			"prefix": string,
			"firstname": string,
			"lastname": string,
			"score": number
		},
		...
	]
}
```
- POST: edit students' assignment score, returns empty json object
	- request body
```json
[
	{
		"student_id": string (require),
		"score": number (require)
	},
	...
]
```


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

### `/teacher_info` DONE
- GET (get teacher profile)
- POST (update teacher profile)

#### body (both request (POST) and response)
```json
{
	"prefix": string
	"firstname": string
	"lastname": string
	"email": string
	"sex": string
	"profile_img": base64 encoded string
}
```

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
	- body
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
