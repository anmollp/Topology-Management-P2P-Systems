# Topology-Management-P2P-Systsems
Topology Management of Overlay Networks

## Setup
*Language used for development:*
  `Python3`


*Directory Structure:*
* dynamic_ring.py
* node.py
* ring.py
* TMAN.py
* TwoDPoint.py
* utils.py
* requirements.txt


**dynamic_ring.py:**
This file contains source code for the dynamic ring topology building and evolution. All methods are described with python doc strings in the class.


**node.py:**
This file contains source code for abstracting the node functionalities. All methods are described with python doc strings in the class.


**ring.py:**
This file contains source code for the ring topology building and evolution. All methods are described with python doc strings in the class.


**TMAN.py:**
This file acts as the driver. In python there is no concept of make files.

To run ring topology:

**Command:** 

`python TMAN.py N k R`
                
To run dynamic_ring topology:

**Command:** 

`python TMAN.py N k D r1 r2 r3 r4 r5 r6 r7 r8`
                
Here **ri** are the radii for every iteration and also denote the ri nodes being added to the topology every 5th iteration.

**TwoDPoint.py:**
This file contains source code for representing a two dimensional coordinate.

**utils.py:**
This file contains all the utility methods such as calculating the color distance, selecting nearest neighbors, writing topologies to text files, etc.      


**requirements.txt:**
This file contains the necessary libraries required to run the code. All of these can be installed by using the command:
        > pip install -r requirements.txt


**Operating System:**
        The OS used for this development is Mac Os (Apple).
**IDE:**
        The code was written in the PyCharm Integrated Development environment. It is preferable that the source code folder be opened in a Pycharm IDE and run to avoid any kind of import issues in the code.


**Python Interpreter Version:**
        The interpreter version used is Python 3.7


**More Info:**
        When the topologies are run, the necessary iteration files and graph images are generated and stored in a directory called Patil_EEL6761_HW1/  under the user’s home directory. If your home directory is /Users/Anmol , then the complete path for the files generated are /Users/Anmol/Patil_EEL6761_HW1/.

## Observations

### a. Explore the following two scenarios for the “ring” topology and describe your findings:
  > i. When a node shares its neighbor-list with a neighbor, only the receiving neighbor will
  update its neighbors-list in each cycle.

*Implementation details:*
File:
  ring.py
Method:
  communicate
Parameters:
  node: the node that initiates communication
  one_way: if true initiate only a one-sided communication
           otherwise a two-way communication
When only the receiving neighbor is updating the neighbor list, for a given topology, say Ring, the number of iterations required to achieve convergence is larger.
For example consider the images below, for N=100, k=9 and color = green. It takes for the ring topology for green color nodes to achieve convergence in the 15th iteration. Here convergence can be understood as the node connections of only the same color.

![image](https://user-images.githubusercontent.com/19925448/153047443-cde100df-9686-45ca-9ce4-28be584b5b58.png)
**Iteration 5**

![image](https://user-images.githubusercontent.com/19925448/153047572-b26c5df8-3f92-4ca3-9ea6-fefbf257f27d.png)
**Iteration 10**

![image](https://user-images.githubusercontent.com/19925448/153047598-43072d7f-bdc1-4860-ab4d-75e03fad54be.png)
Iteration 15

  > ii. When a node shares its neighbor-list with a neighbor, the receiving neighbor will share its neighbors-list to the sending node. Both the sender node and         receiver node(neighbor) will update their neighbors-list in each cycle.
  
  When both sender and receiver nodes are updating their neighbor list, the number of iterations required to achieve convergence is very small. For example for       N=100, k=9 and color=blue, the convergence is right from the 5th iteration
  ![image](https://user-images.githubusercontent.com/19925448/153048038-cd4f6fd2-07a9-44da-aacd-307441d810dd.png)
  **Iteration 1**
  
  ![image](https://user-images.githubusercontent.com/19925448/153048089-f101d572-3a7c-48a5-9f41-5ca1b97a15be.png)
  **Iteration 5**
  
### b. For the “ring” topology with N=100, run your program with different k values. How does the choice of k (the number of neighbors) affect your result? What is the minimum value of k to generate the ring without any disconnects at the end of 40 cycles? Generate 3 node graphs, one showing the connection of red nodes, one showing the connection of green nodes, and one showing the connection of blue nodes.

As the value of k increases the connectivity of the graph also becomes stronger. Given configuration, N = 100. To find the minimum value of k to generate the ring without any disconnects, I have estimated the lower and upper bounds k can take. Lower bound for k assuming every node should have one neighbor. Upper value of k = 34, as a grouping of red, green and blue gives 34, 33 and 33 nodes of each color respectively. And a neighbor size of k = 34 of same colored nodes will definitely be a connected graph.

I am using the function `NetworkX.is_connected(graph)` to detect connectedness for an undirected graph, where NetworkX is the network/graph plotting and analyzing library in python. `graph` is the graph of an individual color(red, green or blue). 
Now performing binary search on 1 to 34 to arrive at the minimum value of k.

```Iteration 1:
start = 1, end = 34
K = 17
Graphs are all connected
Iteration 2:
start = 1, end = 17
K = 9
Graphs are connected
Iteration 3:
start = 1, end = 9
K = 5
Graphs are disconnected.
Iteration 4:
start = 5, end = 9
K = 7
Graphs are disconnected.
Iteration 5:
start = 7, end = 9
K = 8
Graphs are disconnected.
Iteration 6:
K = 9
Graphs are all connected
```

![image](https://user-images.githubusercontent.com/19925448/153048720-1b8dc29d-0fd4-4a14-812f-7f918deddbe1.png)
**Iteration 40 - Red Nodes**

![image](https://user-images.githubusercontent.com/19925448/153048766-d3bb324b-cf21-463c-9709-5b4a392e03da.png)
**Iteration 40 - Blue Nodes**

![image](https://user-images.githubusercontent.com/19925448/153048808-5b365c8e-c6d1-4ec9-9517-7fdf506e1577.png)
**Iteration 40 - Green Nodes**

Sometimes it can be the case that with k < 9, connected graphs are possible but to ensure a fully connected graph in every scenario the connectedness is checked multiple times for the same k. Hence after multiple times if the graph remains connected then it is decided that k is the minimum value for connectedness. Hence, for k = 9 the graphs of all colors are connected. As the value of k increases the connectivity of the graph increases as more number of
neighbors implies more edge connections. Graphs are disconnected.

### c. Can a node’s neighbor list show the same node in multiple entries?
Considering the fact that when two nodes are exchanging the neighbors list, if we allow for duplicate neighbors to exist then, a node's neighbor list will have some same nodes in multiple entries. But in order to achieve the full potential of overlay topology networks, accounting for the duplicate entries in a node's neighbors list and choosing the k nearest neighbors will create a more robust and homogenous network which in several real life use cases can be useful. The implementation part takes care of carefully eliminating these duplicate entries by choosing the common neighbors which are nearer to respective nodes involved in the communication of sharing neighbors list. This implementation is common to both Ring and Dynamic ring topology.
