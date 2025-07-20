import numpy as np
from scipy.optimize import differential_evolution

class RFOptimizer:
    def __init__(self):
        self.optimization_algorithms = ['genetic', 'simulated_annealing', 'particle_swarm']
    
    def optimize_antenna_parameters(self, cell_sites, traffic_patterns):
        '''Optimize antenna tilt, azimuth, and power'''
        
        def objective_function(params):
            # Calculate coverage, capacity, and interference
            coverage_score = self.calculate_coverage(params, cell_sites)
            interference_score = self.calculate_interference(params, cell_sites)
            capacity_score = self.calculate_capacity(params, traffic_patterns)
            
            # Multi-objective optimization
            return -(0.4 * coverage_score + 0.3 * capacity_score - 0.3 * interference_score)
        
        # Parameter bounds: [tilt, azimuth, power] for each site
        bounds = [(0, 15), (0, 360), (20, 43)] * len(cell_sites)
        
        result = differential_evolution(
            objective_function,
            bounds,
            maxiter=1000,
            seed=42
        )
        
        return {
            'optimized_parameters': result.x,
            'optimization_score': -result.fun,
            'convergence': result.success
        }
    def calculate_coverage(self, params, cell_sites):
        '''Calculate coverage score based on antenna parameters'''
        coverage_areas = []
        for i, site in enumerate(cell_sites):
            tilt = params[i * 3]
            azimuth = params[i * 3 + 1] 
            power = params[i * 3 + 2]
            
            # Simplified coverage calculation
            coverage = (power - 20) * (1 + np.cos(np.radians(tilt))) * 0.1
            coverage_areas.append(coverage)
        
        return np.mean(coverage_areas)
    
    def calculate_interference(self, params, cell_sites):
        '''Calculate interference score'''
        total_interference = 0
        for i in range(len(cell_sites)):
            for j in range(i + 1, len(cell_sites)):
                power_i = params[i * 3 + 2]
                power_j = params[j * 3 + 2]
                # Simplified interference calculation
                interference = (power_i * power_j) / (100 + abs(i - j) * 10)
                total_interference += interference
        
        return total_interference / len(cell_sites)
    
    def calculate_capacity(self, params, traffic_patterns):
        '''Calculate capacity score based on traffic patterns'''
        total_capacity = 0
        for i, pattern in enumerate(traffic_patterns):
            power = params[i * 3 + 2] if i * 3 + 2 < len(params) else 30
            # Shannon capacity approximation
            capacity = pattern.get('demand', 1) * np.log2(1 + power / 10)
            total_capacity += capacity
        
        return total_capacity
