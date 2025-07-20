import numpy as np
from scipy import optimize
from typing import Dict, List

class NetworkSliceOrchestrator:
    def __init__(self):
        self.slice_templates = {
            'embb': {'bandwidth_priority': 0.7, 'latency_tolerance': 50},
            'urllc': {'bandwidth_priority': 0.9, 'latency_tolerance': 1},
            'mmtc': {'bandwidth_priority': 0.3, 'latency_tolerance': 1000}
        }
    
    def optimize_slice_allocation(self, demand_vector: Dict) -> Dict:
        '''Dynamic resource allocation using convex optimization'''
        def objective_function(x):
            # Maximize utility while meeting constraints
            utility = sum(np.log(1 + x[i]) for i in range(len(x)))
            return -utility
        
        constraints = [
            {'type': 'ineq', 'fun': lambda x: 100 - sum(x)},  # Bandwidth constraint
            {'type': 'ineq', 'fun': lambda x: min(x)}          # Non-negative allocation
        ]
        
        result = optimize.minimize(
            objective_function,
            x0=[30, 30, 40],  # Initial allocation
            constraints=constraints,
            method='SLSQP'
        )
        
        return {
            'allocation': result.x,
            'optimization_success': result.success,
            'total_utility': -result.fun
        }
