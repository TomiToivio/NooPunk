# Social Graph
Social Graph uses NetworkX and basic methods of Social Network Analysis.
It consists of Nodes and Edges: 
* Node - Node represents a social entity that can also be called an Actor (Actor-Network Theory) or Agent (Agent-Based Model).
* Edge - Edge represents a social collection between two Nodes. Bidirectional Edges mean that both Nodes agree about the nature of the social relationship. Directed Edges mean that the source Node has an opinion about the target Node without the target being aware of the opinion.
Social Graph represents the Network Society and is the basis of the entire NoöPunk Simulation.
The NoöPunk simulation is limited to the area of Helsinki. It also contains some Nodes that are outside the area but active in the society of the area.
Edges represent all meaningful social connections: It doesn't matter if the connection is based on face-to-face interactions in the Physical world, social media friendship in the Cyber, or telepathic connection in the Astral. 

## Nodes
Nodes represent a Person, an Organization, a Faction etc. Nodes represent social entities with an identity and agency. Node can be an organization like a corporation, it cannot be a loose group of people without shared identity or agency. 
Nodes have several attributes: 
* Name: Name of the Node like "Mars Eldrich".
* Type: Type of the Node like "Person" or "Organization".
* ID: ID of the entity that the Node refers to. Constructed by adding the type and name of the Node in lowercase separated by underscores: Person Mars Eldrich would be "person_mars_eldrich". 
Many more attributes are available in the data of the entity.

## Edges
Bidirectional Edges mean mutual connections like friendship or alliance. 
Unidirectional Edges mean that the Target Node is not aware of the opinion of the Source Node or has a different opinion of the Source Node.
They have many attributes: 
* Source: ID of the Source Node.
* Target: ID of the Target Node.
* Value: Ranges from -4 to +4. -4 means hatred, +4 means friendship, love or alliance.
