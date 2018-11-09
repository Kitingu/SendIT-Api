
[![Build Status](https://travis-ci.org/Kitingu/SendIT-Api.svg?branch=master)](https://travis-ci.org/Kitingu/SendIT-Api)

![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/5433b4da514a0011801a/maintainability)](https://codeclimate.com/github/Kitingu/SendIT-Api/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/Kitingu/SendIT-Api/badge.svg)](https://coveralls.io/github/Kitingu/SendIT-Api)

SendIT is a courier service that helps users deliver parcels to different destinations. SendIT provides courier quotes based on weight categories.

## Getting Started
1. Clone the repository to your machine;
    *https://github.com/Kitingu/SendIT-Api.git
2. Open the repo with an IDE of your choice as a project.
## Prerequisites
* Python 3
* Virtual environment.
* Flask
* flask rest-plus
* Postman
* Browser of your choice
## Setup
1 Open terminal. In the root directory;
* Run the command: virtualenv venv -p python3.6,  to create a virtual <br/>
 <br>environment with the name venv. Folder with the name venv will be created<br>
 
<br>Activate the virtual environment by running the command: source /venv/bin/activate<br>
## Application Requirements
* The application requirements are clearly listed in the ***requirents.txt*** document.
   * To install them run the following cmd command:
     * pip install -r requirements.txt
<hr> 
<i>required endpoints</i>
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