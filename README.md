## Log Analyzer - Insight 2017 Challenge.

### Packages used:
Python 

### Data Structures:
Heap, list, dictionary

### Description:
A large http log file has to be analyzed to find interesting access patterns of the website.

### Feature 1
To find most frequent hosts, I gather frequency of each hostname in a dictionary.
Once the dictionary is updated, I update the heap which maintains a list of top 10 max occuring elements.

### Feature 2
Similarly a heap is maintained to keep top 10 resources that consume bandwidth. 
Here I am calculating the bandwidth of a resource by adding up all the bytes for that resource.

### Feature 3
To calculate most frequent hours, first I gather timestamps and their frequencies in a dictionary.
Then I create a window of 1 hour starting from first epoch. Since the timestamps are sorted, 
we can calculate the activity for window starting from every single second.
Again another heap is maintained to keep top 10.

### Feature 4
For each login attempt, we maintain previous two login attempts. If these fall into 20 second window, then we have to block for 5 mins. This is done by keeping a seprate dictionary which stores the resource vs the time it is blocked from. 
