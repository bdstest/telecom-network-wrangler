import numpy as np
from typing import Dict, List, Tuple

class CarrierAggregationOptimizer:
    def __init__(self):
        self.supported_bands = {
            'lte': [700, 850, 1700, 1900, 2100, 2600],  # MHz
            '5g_sub6': [600, 700, 2500, 3500, 3700],    # MHz  
            '5g_mmwave': [28000, 39000]                  # MHz
        }
    
    def optimize_carrier_combination(self, user_requirements: Dict, available_spectrum: Dict) -> Dict:
        '''Optimize carrier aggregation for maximum throughput'''
        
        optimal_combinations = []
        
        for user_id, requirements in user_requirements.items():
            required_throughput = requirements['throughput_mbps']
            location = requirements['location']
            
            # Find best carrier combination
            best_combination = self.find_optimal_carriers(
                required_throughput, 
                location, 
                available_spectrum
            )
            
            optimal_combinations.append({
                'user_id': user_id,
                'primary_carrier': best_combination['primary'],
                'secondary_carriers': best_combination['secondary'],
                'predicted_throughput': best_combination['throughput'],
                'aggregation_efficiency': best_combination['efficiency']
            })
        
        return {
            'optimized_combinations': optimal_combinations,
            'spectrum_utilization': self.calculate_spectrum_efficiency(optimal_combinations),
            'network_capacity_improvement': self.calculate_capacity_gain(optimal_combinations)
        }
    
    def find_optimal_carriers(self, required_throughput: float, location: Tuple, spectrum: Dict) -> Dict:
        '''Find optimal carrier combination for specific requirements'''
        
        # Prioritize carriers based on propagation characteristics
        carrier_scores = {}
        
        for band_type, frequencies in self.supported_bands.items():
            for freq in frequencies:
                if freq in spectrum.get(band_type, []):
                    # Calculate propagation score
                    propagation_score = self.calculate_propagation_score(freq, location)
                    capacity_score = self.calculate_capacity_score(freq, spectrum[band_type][freq])
                    
                    carrier_scores[freq] = {
                        'propagation': propagation_score,
                        'capacity': capacity_score,
                        'combined_score': propagation_score * 0.6 + capacity_score * 0.4
                    }
        
        # Select best combination
        sorted_carriers = sorted(carrier_scores.items(), key=lambda x: x[1]['combined_score'], reverse=True)
        
        primary_carrier = sorted_carriers[0][0]
        secondary_carriers = [carrier[0] for carrier in sorted_carriers[1:4]]  # Up to 3 secondary
        
        predicted_throughput = self.calculate_aggregated_throughput(primary_carrier, secondary_carriers)
        efficiency = min(predicted_throughput / required_throughput, 1.0)
        
        return {
            'primary': primary_carrier,
            'secondary': secondary_carriers,
            'throughput': predicted_throughput,
            'efficiency': efficiency
        }
    
    def calculate_propagation_score(self, frequency: float, location: Tuple) -> float:
        '''Calculate propagation characteristics for frequency and location'''
        # Simplified path loss model
        distance = 1000  # meters - simplified
        path_loss = 20 * np.log10(frequency) + 20 * np.log10(distance) - 147.55
        
        # Higher score for better propagation (lower path loss)
        return max(0, 100 - path_loss) / 100
    
    def calculate_capacity_score(self, frequency: float, bandwidth: float) -> float:
        '''Calculate capacity potential for frequency band'''
        # Shannon capacity estimation
        # Higher frequencies typically support higher bandwidth
        spectral_efficiency = 5.0 if frequency > 3000 else 3.5  # bps/Hz
        
        capacity = bandwidth * spectral_efficiency
        return min(capacity / 1000, 1.0)  # Normalize to 0-1
    
    def calculate_aggregated_throughput(self, primary: float, secondary: List[float]) -> float:
        '''Calculate total throughput from carrier aggregation'''
        # Simplified throughput calculation
        primary_throughput = self.get_carrier_throughput(primary)
        secondary_throughput = sum(self.get_carrier_throughput(freq) * 0.8 for freq in secondary)  # 80% efficiency
        
        return primary_throughput + secondary_throughput
    
    def get_carrier_throughput(self, frequency: float) -> float:
        '''Get theoretical throughput for carrier frequency'''
        # Simplified throughput mapping
        if frequency < 1000:  # Low band
            return 50  # Mbps
        elif frequency < 6000:  # Mid band
            return 150  # Mbps
        else:  # High band / mmWave
            return 1000  # Mbps
