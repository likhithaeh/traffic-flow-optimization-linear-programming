# traffic-flow-optimization-linear-programming

A small Python project that models a city road network as a directed graph and uses linear programming to route traffic so that the busiest road is as empty as possible. It compares this optimized routing against a naive "split evenly at every intersection" rule across four scenarios, and visualizes the result.


METHODOLOGY:

The program follows these steps:

1.Construct the directed road network.
2.Assign a capacity to each road.
3.Select a traffic scenario.
4.Calculate traffic using equal splitting as the baseline.
5.Formulate the traffic problem as a linear programming problem.
6.Use scipy.optimize.linprog to find the optimized flow.
7.Calculate the worst road utilization and excess traffic.
8.Visualize the traffic distribution before and after optimization.
