#!/usr/bin/env python3
"""
GSI Infrastructure Health Monitoring
Comprehensive health monitoring for telecom infrastructure across all generations

Author: bdstest
"""

import json
import asyncio
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

class InfrastructureType(Enum):
    BASE_STATION = "base_station"
    CORE_NETWORK = "core_network"
    BACKHAUL = "backhaul"
    EDGE_COMPUTING = "edge_computing"

class HealthStatus(Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    OFFLINE = "offline"

@dataclass
class InfrastructureElement:
    """Infrastructure element with health metrics"""
    element_id: str
    element_type: InfrastructureType
    generation: str  # 3G, 4G, 5G
    location: str
    health_status: HealthStatus
    cpu_usage_percent: float
    memory_usage_percent: float
    temperature_celsius: float
    uptime_hours: float
    last_maintenance: datetime
    alert_count_24h: int

class GSIInfrastructureMonitor:
    """Global System Infrastructure Health Monitor"""
    
    def __init__(self):
        self.infrastructure_elements = {}
        self.health_thresholds = {
            "cpu_warning": 70,
            "cpu_critical": 90,
            "memory_warning": 75,
            "memory_critical": 95,
            "temp_warning": 65,
            "temp_critical": 80
        }
    
    async def monitor_base_stations(self) -> List[InfrastructureElement]:
        """Monitor base station health across all generations"""
        base_stations = [
            InfrastructureElement(
                element_id="BS_3G_001",
                element_type=InfrastructureType.BASE_STATION,
                generation="3G",
                location="Downtown_Site_A",
                health_status=HealthStatus.HEALTHY,
                cpu_usage_percent=45.2,
                memory_usage_percent=62.1,
                temperature_celsius=42.5,
                uptime_hours=720.5,
                last_maintenance=datetime(2025, 7, 15),
                alert_count_24h=0
            ),
            InfrastructureElement(
                element_id="BS_4G_015",
                element_type=InfrastructureType.BASE_STATION,
                generation="4G",
                location="Suburban_Site_B",
                health_status=HealthStatus.WARNING,
                cpu_usage_percent=78.3,
                memory_usage_percent=71.8,
                temperature_celsius=68.2,
                uptime_hours=1440.2,
                last_maintenance=datetime(2025, 7, 10),
                alert_count_24h=3
            ),
            InfrastructureElement(
                element_id="BS_5G_008",
                element_type=InfrastructureType.BASE_STATION,
                generation="5G",
                location="Business_District_C",
                health_status=HealthStatus.HEALTHY,
                cpu_usage_percent=34.7,
                memory_usage_percent=48.9,
                temperature_celsius=38.1,
                uptime_hours=168.7,
                last_maintenance=datetime(2025, 7, 20),
                alert_count_24h=1
            )
        ]
        
        # Update health status based on metrics
        for station in base_stations:
            station.health_status = self._calculate_health_status(station)
        
        return base_stations
    
    async def monitor_core_network_elements(self) -> List[InfrastructureElement]:
        """Monitor core network elements (MSC, SGSN, MME, AMF)"""
        core_elements = [
            InfrastructureElement(
                element_id="MSC_001",
                element_type=InfrastructureType.CORE_NETWORK,
                generation="3G",
                location="Core_DC_Primary",
                health_status=HealthStatus.HEALTHY,
                cpu_usage_percent=52.1,
                memory_usage_percent=68.4,
                temperature_celsius=35.2,
                uptime_hours=8760.0,  # 1 year
                last_maintenance=datetime(2025, 6, 1),
                alert_count_24h=0
            ),
            InfrastructureElement(
                element_id="MME_002",
                element_type=InfrastructureType.CORE_NETWORK,
                generation="4G",
                location="Core_DC_Primary",
                health_status=HealthStatus.HEALTHY,
                cpu_usage_percent=48.7,
                memory_usage_percent=72.3,
                temperature_celsius=33.8,
                uptime_hours=4380.5,
                last_maintenance=datetime(2025, 7, 5),
                alert_count_24h=1
            ),
            InfrastructureElement(
                element_id="AMF_001",
                element_type=InfrastructureType.CORE_NETWORK,
                generation="5G",
                location="Core_DC_Primary",
                health_status=HealthStatus.WARNING,
                cpu_usage_percent=82.4,
                memory_usage_percent=78.9,
                temperature_celsius=45.6,
                uptime_hours=720.2,
                last_maintenance=datetime(2025, 7, 18),
                alert_count_24h=5
            )
        ]
        
        for element in core_elements:
            element.health_status = self._calculate_health_status(element)
        
        return core_elements
    
    async def monitor_backhaul_network(self) -> List[InfrastructureElement]:
        """Monitor backhaul network infrastructure"""
        backhaul_elements = [
            InfrastructureElement(
                element_id="BH_FIBER_001",
                element_type=InfrastructureType.BACKHAUL,
                generation="Multi-Gen",
                location="Fiber_Ring_North",
                health_status=HealthStatus.HEALTHY,
                cpu_usage_percent=25.3,
                memory_usage_percent=45.7,
                temperature_celsius=28.4,
                uptime_hours=2160.8,
                last_maintenance=datetime(2025, 6, 15),
                alert_count_24h=0
            ),
            InfrastructureElement(
                element_id="BH_MW_005",
                element_type=InfrastructureType.BACKHAUL,
                generation="Multi-Gen",
                location="Microwave_Link_East",
                health_status=HealthStatus.CRITICAL,
                cpu_usage_percent=95.2,
                memory_usage_percent=89.7,
                temperature_celsius=85.1,
                uptime_hours=72.3,
                last_maintenance=datetime(2025, 7, 19),
                alert_count_24h=12
            )
        ]
        
        for element in backhaul_elements:
            element.health_status = self._calculate_health_status(element)
        
        return backhaul_elements
    
    def _calculate_health_status(self, element: InfrastructureElement) -> HealthStatus:
        """Calculate health status based on metrics"""
        critical_conditions = [
            element.cpu_usage_percent >= self.health_thresholds["cpu_critical"],
            element.memory_usage_percent >= self.health_thresholds["memory_critical"],
            element.temperature_celsius >= self.health_thresholds["temp_critical"],
            element.alert_count_24h >= 10
        ]
        
        warning_conditions = [
            element.cpu_usage_percent >= self.health_thresholds["cpu_warning"],
            element.memory_usage_percent >= self.health_thresholds["memory_warning"],
            element.temperature_celsius >= self.health_thresholds["temp_warning"],
            element.alert_count_24h >= 3
        ]
        
        if any(critical_conditions):
            return HealthStatus.CRITICAL
        elif any(warning_conditions):
            return HealthStatus.WARNING
        else:
            return HealthStatus.HEALTHY
    
    async def generate_infrastructure_report(self) -> Dict:
        """Generate comprehensive infrastructure health report"""
        base_stations = await self.monitor_base_stations()
        core_elements = await self.monitor_core_network_elements()
        backhaul_elements = await self.monitor_backhaul_network()
        
        all_elements = base_stations + core_elements + backhaul_elements
        
        # Calculate summary statistics
        status_counts = {}
        for status in HealthStatus:
            status_counts[status.value] = len([e for e in all_elements if e.health_status == status])
        
        generation_health = {}
        for gen in ["3G", "4G", "5G", "Multi-Gen"]:
            gen_elements = [e for e in all_elements if e.generation == gen]
            if gen_elements:
                healthy_count = len([e for e in gen_elements if e.health_status == HealthStatus.HEALTHY])
                generation_health[gen] = {
                    "total_elements": len(gen_elements),
                    "healthy_elements": healthy_count,
                    "health_percentage": round((healthy_count / len(gen_elements)) * 100, 1)
                }
        
        critical_elements = [e for e in all_elements if e.health_status == HealthStatus.CRITICAL]
        
        return {
            "report_timestamp": datetime.utcnow().isoformat(),
            "summary": {
                "total_elements": len(all_elements),
                "status_distribution": status_counts,
                "overall_health_percentage": round((status_counts["healthy"] / len(all_elements)) * 100, 1)
            },
            "generation_health": generation_health,
            "critical_alerts": [
                {
                    "element_id": e.element_id,
                    "type": e.element_type.value,
                    "generation": e.generation,
                    "location": e.location,
                    "issues": self._identify_critical_issues(e)
                }
                for e in critical_elements
            ],
            "maintenance_recommendations": self._generate_maintenance_recommendations(all_elements)
        }
    
    def _identify_critical_issues(self, element: InfrastructureElement) -> List[str]:
        """Identify specific critical issues for an element"""
        issues = []
        
        if element.cpu_usage_percent >= self.health_thresholds["cpu_critical"]:
            issues.append(f"Critical CPU usage: {element.cpu_usage_percent}%")
        
        if element.memory_usage_percent >= self.health_thresholds["memory_critical"]:
            issues.append(f"Critical memory usage: {element.memory_usage_percent}%")
        
        if element.temperature_celsius >= self.health_thresholds["temp_critical"]:
            issues.append(f"Critical temperature: {element.temperature_celsius}°C")
        
        if element.alert_count_24h >= 10:
            issues.append(f"High alert count: {element.alert_count_24h} alerts in 24h")
        
        return issues
    
    def _generate_maintenance_recommendations(self, elements: List[InfrastructureElement]) -> List[str]:
        """Generate maintenance recommendations"""
        recommendations = []
        
        # Find elements needing maintenance
        overdue_maintenance = [
            e for e in elements 
            if (datetime.utcnow() - e.last_maintenance).days > 90
        ]
        
        if overdue_maintenance:
            recommendations.append(f"Schedule maintenance for {len(overdue_maintenance)} overdue elements")
        
        # Check for cooling issues
        hot_elements = [e for e in elements if e.temperature_celsius > 60]
        if hot_elements:
            recommendations.append(f"Investigate cooling systems for {len(hot_elements)} overheating elements")
        
        # Check for performance issues
        high_cpu_elements = [e for e in elements if e.cpu_usage_percent > 80]
        if high_cpu_elements:
            recommendations.append(f"Performance optimization needed for {len(high_cpu_elements)} high-CPU elements")
        
        return recommendations

async def main():
    """Main function for testing infrastructure monitoring"""
    monitor = GSIInfrastructureMonitor()
    
    print("GSI Infrastructure Health Monitor")
    print("=" * 50)
    
    # Generate and display infrastructure report
    report = await monitor.generate_infrastructure_report()
    
    print(f"Total Infrastructure Elements: {report['summary']['total_elements']}")
    print(f"Overall Health: {report['summary']['overall_health_percentage']}%")
    print("\nGeneration Health:")
    for gen, health in report['generation_health'].items():
        print(f"  {gen}: {health['health_percentage']}% ({health['healthy_elements']}/{health['total_elements']})")
    
    if report['critical_alerts']:
        print(f"\nCritical Alerts ({len(report['critical_alerts'])}):")
        for alert in report['critical_alerts']:
            print(f"  {alert['element_id']} ({alert['generation']}): {', '.join(alert['issues'])}")
    
    if report['maintenance_recommendations']:
        print(f"\nMaintenance Recommendations:")
        for rec in report['maintenance_recommendations']:
            print(f"  - {rec}")

if __name__ == "__main__":
    asyncio.run(main())