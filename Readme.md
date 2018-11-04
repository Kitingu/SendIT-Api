SendIT is a courier service that helps users deliver parcels to different destinations. SendIT provides courier quotes based on weight categories.
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
<td> GET /parcels/<parcelId> </td>
<td>Fetch a specific parcel delivery order</td>
</tr>
<tr>
<td>
GET /users/<userId>/parcels
</td>
<td>
Fetch all parcel delivery orders by a specific user</td>
</tr>
<tr>
<td>
PUT /parcels/<parcelId>/cancel</td>
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
