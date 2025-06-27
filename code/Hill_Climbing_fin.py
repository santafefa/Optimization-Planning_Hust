import random
import time
import sys

sys.setrecursionlimit(100000)
class Hill_Climbing:
    def __init__(self, input_file=None):
        self.input_file = input_file
    def read_input(self):
        N,K=map(int, input().split())
        quantity=[]
        cost=[]
        for _ in range(N):
            q,c=map(int, input().split())
            quantity.append(q)
            cost.append(c)
        lower_bound = []
        upper_bound = []
        for _ in range(K):
            l,u=map(int, input().split())
            lower_bound.append(l)
            upper_bound.append(u)
        self.orders_num = N
        self.vehicles_num = K
        self.quantity = quantity
        self.cost = cost
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def check_validation(self, load, v_idx):
        if load == 0:
            return True
        return self.lower_bound[v_idx] <= load <= self.upper_bound[v_idx]
    def greedy(self):
        load = [0] * self.vehicles_num
        assignments = [-1] * self.orders_num
        orders_rate = []
        vehicle_rate = []
        curr_cost = 0
        for idx, cost in enumerate(self.cost):
            orders_rate.append((idx, cost))
        orders_rate.sort(key=lambda x: x[1], reverse=True)

        for ord_idx, _ in orders_rate:
            for veh_idx in range(self.vehicles_num):
                if load[veh_idx] + self.quantity[ord_idx] <= self.upper_bound[veh_idx]:
                    assignments[ord_idx] = veh_idx
                    load[veh_idx] += self.quantity[ord_idx]
                    curr_cost += self.cost[ord_idx]
                    break
        for v_idx in range(self.vehicles_num):
            if load[v_idx] > 0 and load[v_idx] < self.lower_bound[v_idx]:
                for ord_idx, veh_idx in enumerate(assignments):
                    if veh_idx == v_idx:
                        assignments[ord_idx] = -1
                        curr_cost -= self.cost[ord_idx]
                load[v_idx] = 0
        return assignments, load
    def add_unassigned(self, assignments, load):
        unassigned_ord = [i for i, v in enumerate(assignments) if v == -1]
        if not unassigned_ord:
            return None
        add_ord= max(unassigned_ord, key=lambda i: self.cost[i])
        for v_idx in random.sample(range(self.vehicles_num), self.vehicles_num):
            new_load_v= load[v_idx] + self.quantity[add_ord]
            if new_load_v<= self.upper_bound[v_idx]:
                new_assignments = assignments[:]
                new_load = load[:]
                new_assignments[add_ord] = v_idx
                new_load[v_idx] = new_load_v
                return new_assignments, new_load
        return None
    def generate_neighboor_move(self, assignments, load):
        assigned_ord=[i for i,v in enumerate(assignments) if v!=-1]
        if not assigned_ord:
            return None
        remove_ord=random.choice(assigned_ord)
        remove_v=assignments[remove_ord]
        for new_v in random.sample(range(self.vehicles_num), self.vehicles_num):
            if new_v != remove_v:
                if load[new_v] + self.quantity[remove_ord] <= self.upper_bound[new_v]:
                    new_assignments = assignments[:]
                    new_load = load[:]
                    new_load[new_v]+= self.quantity[remove_ord]
                    new_load[remove_v] -= self.quantity[remove_ord]
                    if self.check_validation(new_load[remove_v], remove_v) and self.check_validation(new_load[new_v], new_v):
                        new_assignments[remove_ord] = new_v
                        return new_assignments, new_load
        return None
    def generate_neighboor_swap(self, assignments, load):
        used_vehicles= [i for i, l in enumerate(load) if l > 0]
        if len(used_vehicles) < 2:
            return None
        v1,v2= random.sample(used_vehicles, 2)
        ord_in_v1 = [i for i, v in enumerate(assignments) if v == v1]
        ord_in_v2 = [i for i, v in enumerate(assignments) if v == v2]
        if not ord_in_v1 or not ord_in_v2:
            return None
        ord1 = random.choice(ord_in_v1)
        ord2 = random.choice(ord_in_v2)
        new_load_v1 = load[v1] - self.quantity[ord1] + self.quantity[ord2]
        new_load_v2 = load[v2] + self.quantity[ord1] - self.quantity[ord2]
        if new_load_v1 <= self.upper_bound[v1] and new_load_v2 <= self.upper_bound[v2]:
            if self.check_validation(new_load_v1, v1) and self.check_validation(new_load_v2, v2):
                new_assignments = assignments[:]
                new_load = load[:]
                new_assignments[ord1] = v2
                new_assignments[ord2] = v1
                new_load[v1] = new_load_v1
                new_load[v2] = new_load_v2
                return new_assignments, new_load
        return None
    def solve(self, max_restart=5, max_iterations=850, time_limit=1.0):
        self.read_input()
        start_time = time.time()
        best_assignment = [-1] * self.orders_num
        objective_value = -1
        for _ in range(max_restart):
            if time.time() - start_time > time_limit:
                break
            cur_assign, cur_load = self.greedy()
            for _ in range(max_iterations):
                if time.time() - start_time > time_limit:
                    break
                res= self.add_unassigned(cur_assign, cur_load)
                if res:
                    cur_assign,cur_load = res
                    continue

                if random.random() < 0.5:
                    res = self.generate_neighboor_move(cur_assign,cur_load)
                else:
                    res = self.generate_neighboor_swap(cur_assign,cur_load)
                if res:
                    cur_assign, cur_load = res
            final_load = [0]*self.vehicles_num
            for i, v in enumerate(cur_assign):
                if v != -1:
                    final_load[v] += self.quantity[i]
            final_assign = cur_assign[:]
            for v_idx in range(self.vehicles_num):
                if not self.check_validation(final_load[v_idx], v_idx):
                    for i, v in enumerate(final_assign):
                        if v == v_idx:
                            final_assign[i] = -1
            curr_cost = sum(self.cost[i] for i, v in enumerate(final_assign) if v != -1)
            if curr_cost > objective_value:
                best_assignment = final_assign
                objective_value = curr_cost

        return best_assignment, objective_value

def main():
    solver = Hill_Climbing()
    # Using the robust solve method
    best_assignment, objective_value= solver.solve()
    best_served_orders = [(i + 1, v + 1) for i, v in enumerate(best_assignment) if v != -1]
    # Final Output
    print(len(best_served_orders))
    for order_idx, vehicle_idx in best_served_orders:
        print(f"{order_idx } {vehicle_idx}")
    print(f"Objective Value: {objective_value}")

if __name__ == "__main__":
    main()
