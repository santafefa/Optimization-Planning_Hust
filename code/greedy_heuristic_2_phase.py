class greedy_2_phase:
    def __init__(self, input_file=None):
        self.input_file = input_file
    def read_input(self):
        N,K=map(int, input().split())
        quantiy=[]
        cost=[]
        for _ in range(N):
            q,c=map(int, input().split())
            quantiy.append(q)
            cost.append(c)
        lower_bound = []
        upper_bound = []
        for _ in range(K):
            l,u=map(int, input().split())
            lower_bound.append(l)
            upper_bound.append(u)
        self.orders_num = N
        self.vehicles_num = K
        self.quantiy = quantiy
        self.cost = cost
        self.total_cost=sum(cost)
        self.best_assignment = [-1]*N
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.best_served_orders=0
        self.objective_value = 0

    def plan(self, sorted_orders: str ="cost", sorted_vehicles: str = "lower_bound"):
        assignments = [-1] * self.orders_num
        load = [0] * self.vehicles_num
        orders_rate=[]
        vehicle_rate = []
        curr_cost = 0
        if sorted_orders == "cost":
            for idx, cost in enumerate(self.cost):
                orders_rate.append((idx, cost))
        elif sorted_orders == "weight":
            for idx, weight in enumerate(self.quantiy):
                orders_rate.append((idx, weight))
        elif sorted_orders == "ratio":
            for idx, (weight, cost) in enumerate(zip(self.quantiy, self.cost)):
                orders_rate.append((idx, cost / weight))
        orders_rate.sort(key=lambda x: x[1], reverse=True)
        if sorted_vehicles == "lower_bound":
            for idx, lower in enumerate(self.lower_bound):
                vehicle_rate.append((idx, -lower))
        elif sorted_vehicles == "upper_bound":
            for idx, upper in enumerate(self.upper_bound):
                vehicle_rate.append((idx, -upper))
        elif sorted_vehicles == "range":
            for idx, (lower, upper) in enumerate(zip(self.lower_bound, self.upper_bound)):
                vehicle_rate.append((idx, upper - lower))
        vehicle_rate.sort(key=lambda x: x[1])

        for order_idx, ord_rate in orders_rate:
            for vehicle_idx, v_rate in vehicle_rate:
                if load[vehicle_idx] < self.lower_bound[vehicle_idx] and load[vehicle_idx] + self.quantiy[order_idx] <= self.upper_bound[vehicle_idx]:
                    assignments[order_idx]=vehicle_idx
                    load[vehicle_idx] += self.quantiy[order_idx]
                    curr_cost += self.cost[order_idx]
                    break
        not_satisfied_vehicles = []
        for v_idx in range(self.vehicles_num):
            if load[v_idx] < self.lower_bound[v_idx]:
                for ord_idx, veh_idx in enumerate(assignments):
                    if veh_idx == v_idx:
                        assignments[ord_idx] = -1
                        curr_cost -= self.cost[ord_idx]
                load[v_idx] = 0
                not_satisfied_vehicles.append(v_idx)
        for order_idx, ord_rate in orders_rate:
            if assignments[order_idx] == -1:
                for vehicle_idx, v_rate in vehicle_rate:
                    if vehicle_idx in not_satisfied_vehicles:
                        continue
                    if load[vehicle_idx] + self.quantiy[order_idx] <= self.upper_bound[vehicle_idx]:
                        assignments[order_idx]=vehicle_idx
                        load[vehicle_idx] += self.quantiy[order_idx]
                        curr_cost += self.cost[order_idx]
                        break

        return assignments, curr_cost, load
    def solve(self):
        self.read_input()
        sorted_orders = ["cost", "weight", "ratio"]
        sorted_vehicles = ["lower_bound", "upper_bound", "range"]
        real_load = [0] * self.vehicles_num
        for ord_sort in sorted_orders:
            for veh_sort in sorted_vehicles:
                try:
                    assignment, curr_cost, load = self.plan(ord_sort, veh_sort)
                    if curr_cost > self.objective_value:
                        self.objective_value = curr_cost
                        self.best_assignment = assignment.copy()
                        real_load = load.copy()
                        self.best_served_orders = sum(1 for x in self.best_assignment if x != -1)
                except Exception as e:
                    print(f"Error during planning with order sort {ord_sort} and vehicle sort {veh_sort}: {e}")
                    continue
        return self.best_assignment, self.objective_value, self.best_served_orders, real_load

def main():
    solver = greedy_2_phase()
    best_assignment, objective_value, best_served_orders, real_load = solver.solve()
    print(best_served_orders)
    for o,v in enumerate(best_assignment):
        if v != -1:
            print(f"{o+1} {v+1}")
    print(f"Objective Value: {objective_value}")
    #for i, load in enumerate(real_load):
        #print(f"Vehicle {i+1} load: {load} (should be between {solver.lower_bound[i]} and {solver.upper_bound[i]})")

if __name__ == "__main__":
    main()