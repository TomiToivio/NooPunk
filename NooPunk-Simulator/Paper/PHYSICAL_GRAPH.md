# Physical Graph
Physical Graph is used to represent the Physical world. 
There are two levels of Physical Graphs: 
* City Graph - This represents the map of the City of Helsinki. Nodes are the locations in the city. Edges are the traffic routes between locations. 
* Location Graph - These are locations that can be visited. Nodes represent rooms. Edges represent doors used to enter another room. 

## City Graph
Nodes represent important locations in the city. 
There are several types of Nodes:
* Passive - Passive Nodes are used only for travel. There are no activities available in the node.
* Active - Active Nodes have available activities. They don't open a Physical Graph. 
* Graph - This means visiting the location means you enter another Physical Graph. 

Nodes have the following attributes: 
* Name of the Node. Like Europol Field Office.
* ID - ID of the Node. Based on writing the type of the name of the location in lowercase and replacing spaces with underscores: "location_europol_field_office".
* Address - City address for adding the location to the Map.
* Lat - Coordinates.
* Lon - Coordinates.

Edges represent routes between the locations. 
