from ortools.linear_solver import pywraplp
class ILPSolver:
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
    def solve(self):
        self.read_input()
        solver = pywraplp.Solver.CreateSolver('SCIP')
        #solver.SetTimeLimit(1000 * 2)
        if not solver:
            print("Solver not created.")
            return

        # Variables
        x=[[solver.BoolVar(f'position_{i}_{j}') for j in range(self.vehicles_num)] for i in range(self.orders_num)]
        # Constraints
        y=[solver.BoolVar(f'vehicles_{i}') for i in range(self.vehicles_num)]
        for i in range(self.orders_num):
            solver.Add(sum(x[i][j] for j in range(self.vehicles_num))<=1)

        for j in range(self.vehicles_num):
            solver.Add(sum(x[i][j]*self.quantiy[i] for i in range(self.orders_num)) <= self.upper_bound[j] if y[j] else 0)
            solver.Add(sum(x[i][j]*self.quantiy[i] for i in range(self.orders_num)) >= self.lower_bound[j] if y[j] else 0)

        solver.Maximize(sum(x[i][j]*self.cost[i] for i in range(self.orders_num) for j in range(self.vehicles_num)))
        # Objective
        objective = solver.Objective()
        status = solver.Solve()
        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            print(f"{sum(x[i][j].solution_value() for i in range(self.orders_num) for j in range(self.vehicles_num)):.0f}")
            for i in range(self.orders_num):
                for j in range(self.vehicles_num):
                    if x[i][j].solution_value() > 0:
                        print(f"{i+1} {j+1}")
            #print(f"Objective value: {objective.Value()}")
        else:
            print("No optimal solution found.")

def main():
    solver = ILPSolver()
    solver.solve()
if __name__ == "__main__":
    main()