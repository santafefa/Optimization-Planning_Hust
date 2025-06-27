class back_track:
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
        self.cost_max = min(cost)
    def check_all_lower_bounds(self, load):
        for v_idx in range(self.vehicles_num):
            if 0< load[v_idx] < self.lower_bound[v_idx]:
                return False
        return True
    def plan(self, ord_idx, curr_cost, assignment, load):
        if ord_idx == self.orders_num:
            if self.check_all_lower_bounds(load):
                if curr_cost > self.objective_value:
                    self.objective_value = curr_cost
                    self.best_assignment = assignment.copy()
            return
        for vehicles_idx in range(self.vehicles_num):
            if load[vehicles_idx] + self.quantiy[ord_idx] <= self.upper_bound[vehicles_idx] and assignment[ord_idx] == -1:
                assignment[ord_idx] = vehicles_idx
                load[vehicles_idx] += self.quantiy[ord_idx]
                curr_cost += self.cost[ord_idx]

                self.plan(ord_idx + 1, curr_cost, assignment, load)

                assignment[ord_idx] = -1
                load[vehicles_idx] -= self.quantiy[ord_idx]
                curr_cost -= self.cost[ord_idx]
        self.plan(ord_idx + 1, curr_cost, assignment, load)

    def solve(self):
        self.read_input()
        assignments= [-1] * self.orders_num
        load = [0] * self.vehicles_num
        self.plan(0, 0, assignments, load)
        self.best_served_orders = sum(1 for x in self.best_assignment if x != -1)
        return self.best_assignment, self.objective_value, self.best_served_orders

def main():
    solver = back_track()
    best_assignment, objective_value, best_served_orders = solver.solve()
    print(best_served_orders)
    for o,v in enumerate(best_assignment):
        if v != -1:
            print(f"{o+1} {v+1}")
    #print(f"Objective Value: {objective_value}")

if __name__ == "__main__":
    main()