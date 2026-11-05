# Graphs
NetworkX graphs are used to model the world of NoöPunk. These graphs can be modeled as NetworkX Nodes and Edges. The game situation can also be visualized by drawing the graphs.
In some cases the Nodes of the graph are Agents and the game universe can be simulated with Mesa and/or Concordia.   
There are several types of graphs. These include Physical, Astral, Cyber, Social and Story graphs.
* Physical, Cyber and Astral graphs represent the three levels of reality. In some situations only one of the levels is relevant: Character is traveling through the Physical world or exploring a Physical location, character is using Astral Projection, or character is hacking Cyberspace. In some situation all three graphs are presented as an overlay: Character might be fighting in the Physical while also using PSI in the Astral and hacking in the Cyber against his enemies. 
* Social graph represents the Network Society of NoöPunk. Nodes are characters and factions, Edges represent their social relationships. Edges have values ranging from -4 to +4: -4 means the relationship is one of full antagonism, while +4 represents love, friendship and alliance. Node types include important characters and factions of the NoöPunk campaign. 
* Story graphs represent the Series, Episodes and Scenes: Series Graph represents progress between Episodes (the order of Episodes depends on the choices of the character). Episode Graphs represent stories like important missions. Episodes consist of Scenes. Scene types include Investigation, Exploration, Combat, Social, Cyber and Astral. 

## Social Science
NoöPunk grows out of LaclauGPT (https://github.com/TomiToivio/LaclauGPT/blob/main/paper/PHASE_1_PAPER.md). This is why NoöPunk often uses theories of Social Science as inspiration for the rules. Methods of Social Data Science (like NetworkX) are used to model the NoöPunk world. 
Ernesto Laclau's theory of Discourse Analysis and Ideology (https://en.wikipedia.org/wiki/Ernesto_Laclau) provides the model of ideological struggle in the world of paradigm shifts and ontological shocks. 
Manuel Castells' theory of Network Society (https://en.wikipedia.org/wiki/The_Information_Age:_Economy,_Society_and_Culture) provides the model for NoöPunk's graph-based world.
Niklas Luhmann's cybernetic sociology of Social Systems (https://en.wikipedia.org/wiki/Niklas_Luhmann) is a key inspiration for NoöPunk's model of entangled layers of society: 
* Luhmann's Social Systems -> NoöPunk's Social Graph
* Luhmann's Living Systems -> NoöPunk's Physical Graph
* Luhmann's Psychic Systems -> NoöPunk's Astral Graph
* Luhmann's Machine Systems -> NoöPunk's Cyber Graph

## Physical
The campaign start location is Player's home in the Sörnäinen District of Helsinki.
These graphs represent the physical spacetime on various levels: 
* World - the entire world, Nodes represent locations such as Helsinki and Edges represent routes between them. The World map will only become available when the character has to travel to location outside Helsinki. 
* City - the main city is Helsinki, Nodes represent districts and locations inside Helsinki, Edges represent routes between districts and locations. The locations available in the beginning of the game include Character's home in Sörnäinen and Europol HQ on Ratakatu. 
* Location - location graph Nodes are rooms while Edges are doors between rooms. Outdoors graphs have a bit larger scale, with Nodes as important places in a forest and Edges as paths between these locations. 
We can also present the graphs on top of the map of World or Helsinki, so the locations have map coordinates and addresses. Mission locations can also present the graph overlaid on a map of the location, so the locations have X and Y map coordinates. We may eventually add tactical movement on location maps, but we will consider this later. 

## Astral
NoöPunk's Astral graph is a Conscious Agent Network based on theories of Federico Faggin (Quantum Information Panpsychism) and Donald Hoffman (Conscious Realism). PSI can be seen as similar to Cyberspace hacking: It is just a Quantum Network of Quantum Computers (Conscious Agents).
NoöPunk Psionics are realistic and based on real-world parapsychology, especially Dean Radin (https://en.wikipedia.org/wiki/Dean_Radin). Just like Radin says, PSI is Magick and Magick is PSI.
Astral Projection is an important element of NoöPunk and is based on Robert Monroe's (https://en.wikipedia.org/wiki/Robert_Monroe). Psionics always work through Astral as various types of Conscious Agents interact: It makes no difference if the character is fully active in a Physical location or having an OOBE in the Astral, the Psionics works through the Conscious Agent Network. Andrew Gallimore (https://en.wikipedia.org/wiki/Andrew_Gallimore) brings the idea that DMT allows humans to perceive the Astral Conscious Agent Network directly, which means we want the Astral to look like a psychedelic DMT trip into a multidimensional Hilbert space of Self-Transforming Machine Elves (Conscious Agents). 
Think about Astral as an AR overlay on top of the Physical, or as fully immersive VR when you are having an OOBE. 
NoöPunk uses tweaked SWN Psionics rules for Astral, PSI includes Magick and elements of WWN Magick rules, PSI can also be seen as hacking the Conscious Agent Network, which is why Psionics rules are also similar to CWN Hacking rules. 

## Social
Social Network Graph is for the connections between Factions and important Characters. 
Edges have a score between -4 to +4 representing antagonism of friendship between Nodes.
Factions represent organizations that are important in the campaign: Europol is player's main faction, but it is likely he becomes allied to other factions during the game. 
Important factions include Helsinki City (this is the official government side: most importantly it includes the Helsinki Police representing Law Enforcement, but also other officials of the City Government, and basically everybody who identifies as "the government"). The campaign will have at least four NHI factions (the rogue ASI faction is basically a part of the machine civilization now). Several factions represent local humans who may become allies or enemies: gangs, corporations and political movements.  
Edges are the same as Social Tags in the character sheet: Most important tag attribute is the relationship score between -4 to +4. 
Node attributes can be linked to the entire character sheet of an NPC or Faction.  

## Story Graphs: Series, Episodes and Scenes
Scenes are divided by type into Investigation, Exploration, Combat, Social, Cyber and Astral. Some Scenes have several overlapping types: Character might use hacking (Cyber) and psionics (Astral) in a Combat Scene.  

