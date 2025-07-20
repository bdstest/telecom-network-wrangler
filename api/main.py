from fastapi import FastAPI
from typing import Dict, List
import random
import time
from datetime import datetime
from dataclasses import dataclass
import math

app = FastAPI(title='Network Wrangler API', version='0.1.0')

# Simulation state for realistic metric variations
class MetricsSimulator:
    def __init__(self):
        self.start_time = time.time()
        self.base_sla = 91.0  # Base SLA compliance
        self.base_efficiency = 2.9  # Base spectrum efficiency
        
    def get_time_factor(self) -> float:
        """Get time-based variation factor (daily cycle)"""
        hours = (time.time() - self.start_time) / 3600
        return 0.95 + 0.1 * math.sin(hours * math.pi / 12)  # Daily cycle
        
    def get_network_load(self) -> float:
        """Simulate network load based on time"""
        hours = datetime.now().hour
        if 9 <= hours <= 17:  # Business hours
            return 0.8 + random.uniform(-0.1, 0.15)
        elif 19 <= hours <= 22:  # Evening peak
            return 0.9 + random.uniform(-0.05, 0.1)
        else:  # Off-peak
            return 0.4 + random.uniform(-0.1, 0.2)
            
    def get_sla_compliance(self) -> float:
        """Calculate realistic SLA compliance with variations"""
        base = self.base_sla
        time_factor = self.get_time_factor()
        load_impact = (1 - self.get_network_load()) * 5  # Higher load = lower SLA
        random_variation = random.uniform(-2, 2)
        
        sla = base * time_factor + load_impact + random_variation
        return max(85.0, min(98.0, round(sla, 1)))  # Realistic bounds
        
    def get_spectrum_efficiency(self) -> float:
        """Calculate realistic spectrum efficiency"""
        base = self.base_efficiency
        time_factor = self.get_time_factor()
        load = self.get_network_load()
        
        # Efficiency decreases with high load due to interference
        load_penalty = load * 0.3
        random_variation = random.uniform(-0.2, 0.2)
        
        efficiency = base * time_factor - load_penalty + random_variation
        return max(2.0, min(4.0, round(efficiency, 2)))  # Realistic 5G range
        
simulator = MetricsSimulator()

@app.get('/health')
async def health_check():
    return {'status': 'healthy'}

@app.get('/api/v1/performance/metrics')
async def get_performance_metrics() -> Dict:
    """Get current network performance metrics with dynamic realistic values"""
    sla = simulator.get_sla_compliance()
    efficiency = simulator.get_spectrum_efficiency()
    utilization = simulator.get_network_load() * 100
    
    # Health score derived from SLA and efficiency
    health_score = (sla * 0.6 + (efficiency / 4.0) * 100 * 0.4)
    
    return {
        'health_score': round(health_score, 1),
        'sla_compliance': sla,
        'spectrum_efficiency': efficiency,
        'active_slices': random.randint(38, 47),  # Realistic slice count variation
        'network_utilization': round(utilization, 1),
        'timestamp': datetime.now().isoformat() + 'Z'
    }

@app.get('/api/v1/slicing/performance')
async def get_slice_performance() -> Dict:
    """Get network slice performance metrics with dynamic values"""
    overall_sla = simulator.get_sla_compliance()
    load = simulator.get_network_load()
    
    # Generate realistic per-slice metrics based on overall conditions
    slices = []
    slice_types = [
        {
            'id': 'slice-embb-001',
            'type': 'eMBB',
            'base_sla': overall_sla + random.uniform(-2, 3),
            'base_throughput': 850,
            'base_latency': 12
        },
        {
            'id': 'slice-urllc-001',
            'type': 'URLLC', 
            'base_sla': overall_sla + random.uniform(-5, 1),  # Stricter requirements
            'base_throughput': 100,
            'base_latency': 0.8
        },
        {
            'id': 'slice-mmtc-001',
            'type': 'mMTC',
            'base_sla': overall_sla + random.uniform(-1, 5),  # More lenient
            'base_throughput': 10,
            'base_latency': 100
        }
    ]
    
    for slice_config in slice_types:
        # Apply load impact to metrics
        throughput_factor = 1 - (load - 0.5) * 0.3  # High load reduces throughput
        latency_factor = 1 + (load - 0.5) * 0.4     # High load increases latency
        
        slices.append({
            'id': slice_config['id'],
            'type': slice_config['type'],
            'sla_compliance': round(max(80, min(98, slice_config['base_sla'])), 1),
            'throughput': round(slice_config['base_throughput'] * throughput_factor, 1),
            'latency': round(slice_config['base_latency'] * latency_factor, 2),
            'availability': round(99.5 + random.uniform(-0.3, 0.5), 2)
        })
    
    return {
        'slices': slices,
        'overall_compliance': overall_sla,
        'timestamp': datetime.now().isoformat() + 'Z'
    }

@app.get('/api/v1/spectrum/analysis')
async def get_spectrum_analysis() -> Dict:
    """Get spectrum analysis metrics"""
    efficiency = simulator.get_spectrum_efficiency()
    
    frequency_bands = [
        {'band': '700MHz', 'efficiency': efficiency + random.uniform(-0.3, 0.2)},
        {'band': '1800MHz', 'efficiency': efficiency + random.uniform(-0.2, 0.3)},
        {'band': '2100MHz', 'efficiency': efficiency + random.uniform(-0.1, 0.4)},
        {'band': '2600MHz', 'efficiency': efficiency + random.uniform(0.1, 0.5)},
        {'band': '3500MHz', 'efficiency': efficiency + random.uniform(0.2, 0.6)},
        {'band': '28GHz', 'efficiency': efficiency + random.uniform(0.5, 1.0)}
    ]
    
    return {
        'overall_efficiency': efficiency,
        'frequency_bands': [
            {**band, 'efficiency': round(max(1.5, min(5.0, band['efficiency'])), 2)}
            for band in frequency_bands
        ],
        'optimization_status': 'active' if random.random() > 0.3 else 'idle',
        'timestamp': datetime.now().isoformat() + 'Z'
    }

@app.get('/api/v1/network/capacity')
async def get_capacity_metrics() -> Dict:
    """Get network capacity and planning metrics"""
    load = simulator.get_network_load()
    
    return {
        'current_utilization': round(load * 100, 1),
        'capacity_threshold_warning': 80.0,
        'capacity_threshold_critical': 95.0,
        'predicted_peak_hours': [9, 10, 11, 19, 20, 21],
        'remaining_capacity': round((1 - load) * 100, 1),
        'capacity_planning': {
            'next_7_days': round(load * 100 + random.uniform(-5, 10), 1),
            'next_30_days': round(load * 100 + random.uniform(-10, 15), 1)
        },
        'timestamp': datetime.now().isoformat() + 'Z'
    }

@app.get('/api/v1/alerts/active')
async def get_active_alerts() -> Dict:
    """Get current network alerts and issues"""
    sla = simulator.get_sla_compliance()
    load = simulator.get_network_load()
    
    alerts = []
    
    # Generate realistic alerts based on current conditions
    if sla < 88:
        alerts.append({
            'id': 'sla-001',
            'severity': 'high',
            'type': 'SLA_VIOLATION',
            'message': f'SLA compliance dropped to {sla}%',
            'timestamp': datetime.now().isoformat() + 'Z'
        })
    
    if load > 0.9:
        alerts.append({
            'id': 'cap-001',
            'severity': 'warning',
            'type': 'HIGH_UTILIZATION',
            'message': f'Network utilization at {round(load*100, 1)}%',
            'timestamp': datetime.now().isoformat() + 'Z'
        })
    
    # Random operational alerts
    if random.random() < 0.3:
        alerts.append({
            'id': f'opt-{random.randint(100, 999)}',
            'severity': 'info',
            'type': 'OPTIMIZATION_COMPLETE',
            'message': 'RF optimization cycle completed successfully',
            'timestamp': datetime.now().isoformat() + 'Z'
        })
    
    return {
        'alerts': alerts,
        'total_active': len(alerts),
        'timestamp': datetime.now().isoformat() + 'Z'
    }
