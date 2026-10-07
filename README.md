# traffic-flow-optimization-linear-programming

A small Python project that models a city road network as a directed graph and uses linear programming to route traffic so that the busiest road is as empty as possible. It compares this optimized routing against a naive "split evenly at every intersection" rule across four scenarios, and visualizes the result.


STRATEGIES:

Two routing strategies are compared. The baseline ("before") has every intersection split its incoming cars equally among its outgoing roads, ignoring capacity. The optimized routing ("after") uses a linear program to choose the flow on every road so that the utilisation of the most heavily loaded road is as low as possible.

SCENARIOS:

The model is tested on four scenarios. In the Normal scenario, 770 cars per hour travel from A to F. In Peak Hour, demand rises to 850 cars per hour. In Road Closure, road B→D is closed, forcing traffic onto the remaining routes. In Reduced Capacity, the capacity of road D→E drops from 600 to 250 cars per hour.


VISUALISATION:

- **Green:** under 80% of capacity (flowing comfortably)
- **Orange:** 80% of capacity or more, but within the limit (busy, near congestion)
- **Red:** over capacity (overloaded)
