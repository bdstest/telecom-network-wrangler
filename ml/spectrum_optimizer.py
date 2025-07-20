"""
Advanced Spectrum Optimization Engine
Implements machine learning algorithms for dynamic spectrum allocation and interference mitigation
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from scipy.optimize import differential_evolution
import logging

logger = logging.getLogger(__name__)


class SpectrumOptimizer:
    """
    Comprehensive spectrum optimization using ML-driven interference prediction
    and dynamic allocation algorithms
    """
    
    def __init__(self):
        self.interference_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.allocation_history = []
        self.frequency_bands = {
            'low_band': {'range': (700, 900), 'characteristics': 'wide_coverage'},
            'mid_band': {'range': (1800, 2600), 'characteristics': 'balanced'},
            'high_band': {'range': (3400, 3800), 'characteristics': 'high_capacity'},
            'mmwave': {'range': (26000, 29000), 'characteristics': 'ultra_capacity'}
        }
    
    def analyze_spectrum_utilization(self, measurements: pd.DataFrame) -> Dict:
        """
        Analyze current spectrum utilization patterns across frequency bands
        
        Args:
            measurements: DataFrame with columns ['frequency', 'power', 'timestamp', 'cell_id']
        
        Returns:
            Dict containing utilization metrics and recommendations
        """
        utilization_stats = {}
        
        for band_name, band_info in self.frequency_bands.items():
            freq_min, freq_max = band_info['range']
            band_data = measurements[
                (measurements['frequency'] >= freq_min) & 
                (measurements['frequency'] <= freq_max)
            ]
            
            if not band_data.empty:
                utilization = self._calculate_band_utilization(band_data)
                efficiency = self._calculate_spectral_efficiency(band_data)
                interference = self._detect_interference(band_data)
                
                utilization_stats[band_name] = {
                    'utilization_percentage': utilization,
                    'spectral_efficiency': efficiency,
                    'interference_level': interference,
                    'recommendation': self._generate_recommendation(utilization, interference)
                }
        
        return utilization_stats
    
    def optimize_carrier_aggregation(self, user_requirements: List[Dict]) -> Dict:
        """
        Optimize carrier aggregation configuration for multiple users
        
        Args:
            user_requirements: List of dicts with user QoS requirements
        
        Returns:
            Optimized carrier aggregation configuration
        """
        def objective_function(x):
            """Objective function for carrier aggregation optimization"""
            total_cost = 0
            for i, user in enumerate(user_requirements):
                required_throughput = user['required_throughput']
                allocated_carriers = x[i * 3:(i + 1) * 3]  # 3 carriers per user
                
                achieved_throughput = self._calculate_throughput(allocated_carriers)
                
                # Penalty for not meeting requirements
                if achieved_throughput < required_throughput:
                    total_cost += (required_throughput - achieved_throughput) ** 2
                
                # Cost for using spectrum resources
                total_cost += np.sum(allocated_carriers) * 0.1
            
            return total_cost
        
        # Optimization bounds (0-1 for each carrier allocation)
        bounds = [(0, 1) for _ in range(len(user_requirements) * 3)]
        
        result = differential_evolution(
            objective_function, 
            bounds, 
            maxiter=1000,
            seed=42
        )
        
        return {
            'optimized_allocation': result.x,
            'optimization_score': result.fun,
            'convergence': result.success
        }
    
    def predict_interference(self, 
                           network_topology: Dict, 
                           proposed_allocation: Dict) -> float:
        """
        Predict interference levels for proposed spectrum allocation
        
        Args:
            network_topology: Network cell layout and parameters
            proposed_allocation: Proposed frequency allocation
        
        Returns:
            Predicted interference level (0-1 scale)
        """
        features = self._extract_interference_features(network_topology, proposed_allocation)
        
        if hasattr(self.interference_model, 'predict'):
            interference_prediction = self.interference_model.predict([features])[0]
        else:
            # Fallback calculation for untrained model
            interference_prediction = self._calculate_theoretical_interference(
                network_topology, proposed_allocation
            )
        
        return np.clip(interference_prediction, 0, 1)
    
    def dynamic_frequency_assignment(self, 
                                   cells: List[Dict], 
                                   traffic_demand: Dict) -> Dict:
        """
        Dynamic frequency assignment based on traffic patterns and interference
        
        Args:
            cells: List of cell configurations
            traffic_demand: Current traffic demand per cell
        
        Returns:
            Optimized frequency assignment plan
        """
        assignment_plan = {}
        
        # Cluster cells based on geographic proximity and traffic patterns
        cell_features = np.array([
            [cell['lat'], cell['lon'], traffic_demand.get(cell['id'], 0)]
            for cell in cells
        ])
        
        kmeans = KMeans(n_clusters=min(5, len(cells)), random_state=42)
        cell_clusters = kmeans.fit_predict(cell_features)
        
        for cluster_id in np.unique(cell_clusters):
            cluster_cells = [cells[i] for i in np.where(cell_clusters == cluster_id)[0]]
            
            # Assign frequencies within cluster to minimize interference
            frequencies = self._assign_cluster_frequencies(cluster_cells, traffic_demand)
            
            for cell, freq in zip(cluster_cells, frequencies):
                assignment_plan[cell['id']] = {
                    'primary_frequency': freq['primary'],
                    'secondary_frequencies': freq['secondary'],
                    'power_level': freq['power'],
                    'cluster': cluster_id
                }
        
        return assignment_plan
    
    def _calculate_band_utilization(self, band_data: pd.DataFrame) -> float:
        """Calculate spectrum utilization for a frequency band"""
        if band_data.empty:
            return 0.0
        
        # Calculate based on power levels above noise floor
        noise_floor = -110  # dBm
        active_measurements = band_data[band_data['power'] > noise_floor]
        
        utilization = len(active_measurements) / len(band_data) * 100
        return min(utilization, 100.0)
    
    def _calculate_spectral_efficiency(self, band_data: pd.DataFrame) -> float:
        """Calculate spectral efficiency in bps/Hz"""
        if band_data.empty:
            return 0.0
        
        # Simplified calculation based on SINR and modulation
        avg_sinr = band_data['power'].mean() - (-110)  # Simplified SINR
        
        # Shannon capacity approximation
        spectral_efficiency = np.log2(1 + 10**(avg_sinr/10))
        
        return min(spectral_efficiency, 4.5)  # Cap at realistic 5G maximum
    
    def _detect_interference(self, band_data: pd.DataFrame) -> str:
        """Detect interference patterns in frequency band"""
        if band_data.empty:
            return "low"
        
        power_std = band_data['power'].std()
        
        if power_std > 10:
            return "high"
        elif power_std > 5:
            return "medium"
        else:
            return "low"
    
    def _generate_recommendation(self, utilization: float, interference: str) -> str:
        """Generate optimization recommendation"""
        if utilization > 80 and interference == "high":
            return "Consider load balancing to adjacent bands"
        elif utilization < 40:
            return "Band underutilized - opportunity for capacity optimization"
        elif interference == "high":
            return "Implement interference mitigation techniques"
        else:
            return "Operating within optimal parameters"
    
    def _calculate_throughput(self, allocated_carriers: np.ndarray) -> float:
        """Calculate throughput based on allocated carriers"""
        # Simplified throughput calculation
        bandwidth_per_carrier = 20  # MHz
        total_bandwidth = np.sum(allocated_carriers) * bandwidth_per_carrier
        spectral_efficiency = 2.9  # bps/Hz realistic for 5G production networks
        
        return total_bandwidth * spectral_efficiency  # Mbps
    
    def _extract_interference_features(self, 
                                     topology: Dict, 
                                     allocation: Dict) -> List[float]:
        """Extract features for interference prediction"""
        features = [
            len(topology.get('cells', [])),  # Number of cells
            allocation.get('frequency_reuse_factor', 1),  # Reuse factor
            topology.get('average_cell_distance', 1000),  # Average inter-cell distance
            allocation.get('power_level', 43),  # Transmission power
            len(allocation.get('allocated_frequencies', [])),  # Number of frequencies
        ]
        
        return features
    
    def _calculate_theoretical_interference(self, 
                                          topology: Dict, 
                                          allocation: Dict) -> float:
        """Calculate theoretical interference when model is not trained"""
        reuse_factor = allocation.get('frequency_reuse_factor', 1)
        cell_density = len(topology.get('cells', [])) / topology.get('coverage_area', 1000)
        
        # Simplified interference calculation
        interference = (cell_density * 0.1) / reuse_factor
        
        return min(interference, 1.0)
    
    def _assign_cluster_frequencies(self, 
                                   cluster_cells: List[Dict], 
                                   traffic_demand: Dict) -> List[Dict]:
        """Assign frequencies within a cell cluster"""
        frequencies = []
        available_freqs = list(range(1, 21))  # 20 available frequency channels
        
        for i, cell in enumerate(cluster_cells):
            demand = traffic_demand.get(cell['id'], 1)
            
            # Assign primary frequency based on position in cluster
            primary_freq = available_freqs[i % len(available_freqs)]
            
            # Assign secondary frequencies based on demand
            secondary_count = min(int(demand / 10), 3)  # Max 3 secondary frequencies
            secondary_freqs = [
                available_freqs[(i + j + 1) % len(available_freqs)] 
                for j in range(secondary_count)
            ]
            
            # Power level based on demand and interference considerations
            power_level = min(43, 20 + demand * 0.5)  # Max 43 dBm
            
            frequencies.append({
                'primary': primary_freq,
                'secondary': secondary_freqs,
                'power': power_level
            })
        
        return frequencies