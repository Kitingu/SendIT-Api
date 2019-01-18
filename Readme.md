
[![Build Status](https://travis-ci.com/Kitingu/SendIT-Api.svg?branch=develop)](https://travis-ci.com/Kitingu/SendIT-Api)
![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/5433b4da514a0011801a/maintainability)](https://codeclimate.com/github/Kitingu/SendIT-Api/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/Kitingu/SendIT-Api/badge.svg?branch=develop)](https://coveralls.io/github/Kitingu/SendIT-Api?branch=develop)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/183700ca76f346e5b5b4ca98eb8109ed)](https://www.codacy.com/app/Kitingu/SendIT-Api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Kitingu/SendIT-Api&amp;utm_campaign=Badge_Grade)

SendIT is a courier service that helps users deliver parcels to different destinations. SendIT provides courier quotes based on weight categories.
### Prerequisites
*Python 3*

*Virtual environment*

*Flask*

*Flask rest-plus*

*Postman*

*A browser of your choice*



# Getting Started
1. Clone the repository to your machine;
  ```
      https://github.com/Kitingu/SendIT-Api.git
```
    

2. Initialize and activate a virtualenv:
  ```
      $ virtualenv venv -p python3
      $ source venv/bin/activate
  ```

3. Install the dependencies:
  ```
      $ pip install -r requirements.txt
  ```

5. Run the development server:

  ```
      $ export FLASK_APP=run.py
  ```
  ```
      $ flask run
  ```
<hr>
<i>Endpoints</i>
<table>
<th>EndPoint </th>
<th> Functionality</th>
<tr>
<td>GET /parcels</td>
<td>Fetch all parcel delivery orders</td>
</tr>
<tr>  
<td> GET /parcels/{parcel_Id} </td>
<td>Fetch a specific parcel delivery order</td>
</tr>
<tr>
<td>
GET /users/{userId}/parcels
</td>
<td>
Fetch all parcel delivery orders by a specific user</td>
</tr>
<tr>
<td>
PUT /parcels/{parcel_Id}/cancel</td>
<td>
Cancel the specific parcel delivery order</td>
</tr>
<tr>
<td>
POST /parcels</td>
<td>
Create a parcel delivery order
</td>
</tr>
<table>


### Built with :

<a href="http://flask.pocoo.org/"><img
   src="http://flask.pocoo.org/static/badges/powered-by-flask-s.png"
   border="0"
   alt="powered by Flask"
   title="powered by Flask"></a>

### Running tests
```
To check if all tests pass - $ pytest
To check the test Coverage - $nosetests --with-coverage --cover-package=app
```

### Documentation:
[Heroku](https://senditapi-v2.herokuapp.com/api/v2/)

### Author:
Benedict Mwendwa

### License
MIT License
