from ortools.sat.python import cp_model
class CPSolver:
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
        self.quantity = quantiy
        self.cost = cost
        self.total_cost=sum(cost)
        self.best_assignment = [-1]*N
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.best_served_orders=0
        self.objective_value = 0
    def solve(self):
        self.read_input()
        model= cp_model.CpModel()
        if not model:
            print("Model not created.")
            return
        # Variables
        x=[[model.NewBoolVar(f'position_{i}_{j}') for j in range(self.vehicles_num)] for i in range(self.orders_num)]
        # Constraints
        y=[model.NewBoolVar(f'vehicles_{i}') for i in range(self.vehicles_num)]
        for i in range(self.orders_num):
            model.Add(sum(x[i][j] for j in range(self.vehicles_num)) <= 1)
        for j in range(self.vehicles_num):
            load_j= sum(x[i][j] * self.quantity[i] for i in range(self.orders_num))
            model.Add(load_j <= self.upper_bound[j]).OnlyEnforceIf(y[j])
            model.Add(load_j >= self.lower_bound[j]).OnlyEnforceIf(y[j])
            model.Add(load_j == 0).OnlyEnforceIf(y[j].Not())

        model.Maximize(sum(x[i][j] * self.cost[i] for i in range(self.orders_num) for j in range(self.vehicles_num)))
        solver= cp_model.CpSolver()
        status = solver.Solve(model)
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print(f"{sum(solver.Value(x[i][j]) for i in range(self.orders_num) for j in range(self.vehicles_num)):.0f}")
            for i in range(self.orders_num):
                for j in range(self.vehicles_num):
                    if solver.Value(x[i][j]) > 0:
                        print(f"{i+1} {j+1}")
            #print(f"Objective value: {solver.ObjectiveValue()}")
        else:
            print("No solution found.")
def main():
    solver = CPSolver()
    solver.solve()
if __name__ == "__main__":
    main()
