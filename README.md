# Event-Evolution-Graphs-of-Historic-Events

A huge amount of data avaialable today is in the form of text. If we consider the history of the world over the past, a number of events have took place that in some form helped to shape the world that we live in today. These events, which may even seem insignificant might had been given rise to another event to take place. These events play an important role in Natural Language Processing. Event Evolution Graphs are the graphs that show relationships between different events in a well defined structure. Here, a knowledge graph of events that have happened from the 17th century to the 18th century is created to find relations between various entities.

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

