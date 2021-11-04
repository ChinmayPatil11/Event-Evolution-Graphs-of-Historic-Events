# Event-Evolution-Graphs-of-Historic-Events

A huge amount of data available today is in the form of text. If we consider the history of the world over the past, a number of events have took place that in some form helped to shape the world that we live in today. These events, which may even seem insignificant might had been given rise to another event to take place. These events play an important role in Natural Language Processing. Event Evolution Graphs are the graphs that show relationships between different events in a well defined structure. Here, a knowledge graph of events that have happened from the 17th century to the 18th century is created to find relations between various entities.

Check out the project here!  
[Event Evolution Graph](https://event-evolution-graph.herokuapp.com/)

### How it works
- The entire network is displayed. Click on any node in the network to see what it is and the different nodes it is connected to.
    - Purple node is the selected node.
    - Blue nodes and edges are the incoming nodes and edges respectively.
    - Red nodes and edges are the outgoing nodes and edges respectively.
- The same is displayed in the table where the source and target node along with their relation is described.
- Also, you can check a node if it is present in the network or not.
    - If the node is present, it lists all the nodes and highlights them in the network with the same convention of colors.
    - If the node is absent, it will say that the node is absent.
- Above the graph, there is a slider which can be adjusted to specify the events occuring only in that year range to appear in the graph. In the beginning, the range is set from 1600 to 1900 which is currently all the years. This can be adjusted according to the needs to look only at a specific decade or a century.

### Description

- Scraped the data from Wikipedia.
- Created a knowledge graph from the scraped data.
- Extracted subject-relation-object triplets from every sentence in data.
- Used Networkx to create a MultiDiGraph with subjects and objects as verbs and relations as edge attribute.
- Used dash to create a dashboard showing the graph.

### Data Collection

The data was web scraped from wikipedia from a few different pages using *BeautifulSoup* and *Requests* library. The scraped data was converted in a csv file for easier handling and reading with the help of pandas. Currently, the data is extracted from 3 urls for the 17th, 18th and 19th century. The links are:  
- [17th Century](https://en.wikipedia.org/wiki/Timeline_of_the_17th_century)  
- [18th Century](https://en.wikipedia.org/wiki/Timeline_of_the_18th_century)  
- [19th Century](https://en.wikipedia.org/wiki/Timeline_of_the_17th_century)  

