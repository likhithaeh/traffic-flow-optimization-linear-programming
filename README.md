# traffic-flow-optimization-linear-programming

A small Python project that models a city road network as a directed graph and uses linear programming to route traffic so that the busiest road is as empty as possible. It compares this optimized routing against a naive "split evenly at every intersection" rule across four scenarios, and visualizes the result.


STRATEGIES:

Two routing strategies are compared. The baseline ("before") has every intersection split its incoming cars equally among its outgoing roads, ignoring capacity. The optimized routing ("after") uses a linear program to choose the flow on every road so that the utilisation of the most heavily loaded road is as low as possible.

SCENARIOS:

The model is tested on four scenarios. In the Normal scenario, 770 cars per hour travel from A to F. In Peak Hour, demand rises to 850 cars per hour. In Road Closure, road B→D is closed, forcing traffic onto the remaining routes. In Reduced Capacity, the capacity of road D→E drops from 600 to 250 cars per hour.

PROGRAM FLOW:

1. **Define the network:** Six intersections (A to F) joined by nine one-way roads with capacities.
2. **Build each scenario:** Normal, Peak Hour, Road Closure and Reduced Capacity each adjust the demand or the roads.
3. **Baseline routing:** Every intersection splits its cars equally among its exits.
4. **Optimized routing:** A linear program routes cars to minimize the busiest road's utilisation.
5. **Compare:** Worst utilisation and excess cars are calculated for both strategies and printed.
6. **Visualize:** The chosen scenario is drawn before and after, then saved as traffic_result.png.


VISUALISATION:

- **Green:** under 80% of capacity (flowing comfortably)
- **Orange:** 80% of capacity or more, but within the limit (busy, near congestion)
- **Red:** over capacity (overloaded)
