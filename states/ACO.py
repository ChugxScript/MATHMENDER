import numpy as np

class AntColonyOptimization:
    def __init__(self, equations, num_ants=10, max_iter=100, evaporation_rate=0.5, pheromone_deposit=1.0):
        self.equations = equations
        self.num_ants = num_ants
        self.max_iter = max_iter
        self.evaporation_rate = evaporation_rate
        self.pheromone_deposit = pheromone_deposit
        self.pheromone = np.ones(len(equations))
    
    def select_equations(self):
        probabilities = self.pheromone / np.sum(self.pheromone)
        selected_indices = []
        for i in range(len(self.equations)):
            if np.random.rand() < probabilities[i]:
                selected_indices.append(i)
        return selected_indices
    
    def update_pheromone(self, solutions, scores):
        self.pheromone *= (1 - self.evaporation_rate)
        for solution, score in zip(solutions, scores):
            for eq_index in solution:
                self.pheromone[eq_index] += self.pheromone_deposit * (score / max(scores))
    
    def run(self):
        best_solution = None
        best_score = float('-inf')
        
        for iter in range(self.max_iter):
            solutions = []
            scores = []
            
            for ant in range(self.num_ants):
                solution = self.select_equations()
                score = sum(self.equations[i]['eq_score'] for i in solution)
                
                solutions.append(solution)
                scores.append(score)
                
                if score > best_score:
                    best_solution = solution
                    best_score = score
            
            # print(f"Iteration {iter+1}: Best Score = {best_score}")
            self.update_pheromone(solutions, scores)
        
        return best_solution, best_score