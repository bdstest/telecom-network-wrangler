from typing import Dict, List
from enum import Enum

class NetworkGeneration(Enum):
    GSM_2G = '2G'
    UMTS_3G = '3G'
    LTE_4G = '4G'
    NR_5G = '5G'

class MultiGenerationAuditor:
    def __init__(self):
        self.generation_capabilities = {
            NetworkGeneration.GSM_2G: {
                'max_throughput': 0.384,  # Mbps (EDGE)
                'technologies': ['GSM', 'GPRS', 'EDGE'],
                'frequencies': [850, 900, 1800, 1900],  # MHz
                'coverage_radius': 35000  # meters
            },
            NetworkGeneration.UMTS_3G: {
                'max_throughput': 42,  # Mbps (HSPA+)
                'technologies': ['UMTS', 'HSPA', 'HSPA+'],
                'frequencies': [850, 900, 1900, 2100],  # MHz
                'coverage_radius': 20000  # meters
            },
            NetworkGeneration.LTE_4G: {
                'max_throughput': 1000,  # Mbps (LTE-A)
                'technologies': ['LTE', 'LTE-A', 'LTE-A Pro'],
                'frequencies': [700, 850, 1700, 1900, 2100, 2600],  # MHz
                'coverage_radius': 15000  # meters
            },
            NetworkGeneration.NR_5G: {
                'max_throughput': 10000,  # Mbps (theoretical)
                'technologies': ['5G NR', '5G SA', '5G NSA'],
                'frequencies': [600, 700, 2500, 3500, 28000, 39000],  # MHz
                'coverage_radius': {'sub6': 10000, 'mmwave': 1000}  # meters
            }
        }
    
    def audit_network_evolution(self, current_infrastructure: Dict) -> Dict:
        '''Audit network infrastructure across all generations'''
        
        audit_results = {}
        
        for generation in NetworkGeneration:
            generation_audit = self.audit_generation(generation, current_infrastructure)
            audit_results[generation.value] = generation_audit
        
        migration_recommendations = self.generate_migration_recommendations(audit_results)
        
        return {
            'generation_audits': audit_results,
            'migration_recommendations': migration_recommendations,
            'modernization_score': self.calculate_modernization_score(audit_results),
            'spectrum_efficiency_evolution': self.analyze_spectrum_efficiency_evolution(audit_results)
        }
    
    def audit_generation(self, generation: NetworkGeneration, infrastructure: Dict) -> Dict:
        '''Audit specific network generation'''
        
        generation_info = self.generation_capabilities[generation]
        deployed_sites = infrastructure.get(generation.value.lower(), {})
        
        return {
            'deployment_status': self.assess_deployment_status(deployed_sites),
            'coverage_analysis': self.analyze_coverage(deployed_sites, generation_info),
            'capacity_utilization': self.analyze_capacity_utilization(deployed_sites, generation_info),
            'technology_mix': self.analyze_technology_mix(deployed_sites, generation_info),
            'spectrum_allocation': self.analyze_spectrum_allocation(deployed_sites, generation_info),
            'modernization_opportunities': self.identify_modernization_opportunities(deployed_sites, generation)
        }
    
    def generate_migration_recommendations(self, audit_results: Dict) -> List[Dict]:
        '''Generate recommendations for network evolution'''
        
        recommendations = []
        
        # Check for 2G/3G sunset opportunities
        if audit_results.get('2G', {}).get('capacity_utilization', 0) < 10:
            recommendations.append({
                'priority': 'high',
                'action': '2G shutdown and spectrum refarming',
                'benefit': 'Reallocate spectrum to 4G/5G for capacity increase',
                'timeline': '6-12 months'
            })
        
        if audit_results.get('3G', {}).get('capacity_utilization', 0) < 20:
            recommendations.append({
                'priority': 'medium',
                'action': '3G network consolidation',
                'benefit': 'Reduce operational costs and improve spectrum efficiency',
                'timeline': '12-18 months'
            })
        
        # 5G deployment recommendations
        lte_utilization = audit_results.get('4G', {}).get('capacity_utilization', 0)
        if lte_utilization > 70:
            recommendations.append({
                'priority': 'high',
                'action': '5G capacity layer deployment',
                'benefit': 'Offload LTE traffic and provide enhanced services',
                'timeline': '6-24 months'
            })
        
        return recommendations
    
    def calculate_modernization_score(self, audit_results: Dict) -> float:
        '''Calculate overall network modernization score (0-100)'''
        
        scores = []
        weights = {'2G': 0.1, '3G': 0.2, '4G': 0.4, '5G': 0.3}
        
        for generation, weight in weights.items():
            if generation in audit_results:
                generation_score = self.calculate_generation_score(audit_results[generation])
                scores.append(generation_score * weight)
        
        return sum(scores)
    
    def analyze_spectrum_efficiency_evolution(self, audit_results: Dict) -> Dict:
        '''Analyze spectrum efficiency improvements across generations'''
        
        efficiency_evolution = {}
        
        for generation in ['2G', '3G', '4G', '5G']:
            if generation in audit_results:
                efficiency = self.calculate_spectrum_efficiency(audit_results[generation])
                efficiency_evolution[generation] = {
                    'spectral_efficiency': efficiency,
                    'improvement_factor': efficiency / 0.1 if generation != '2G' else 1.0  # Relative to 2G baseline
                }
        
        return efficiency_evolution
