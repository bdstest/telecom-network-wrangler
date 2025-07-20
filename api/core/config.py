"""
Application configuration settings
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://telecom_user:5G_network_2024!@localhost:5432/network_monitoring"
    
    # Redis
    REDIS_URL: str = "redis://:5G_cache_2024@localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "telecom_network_wrangler_secret_key_2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080"
    ]
    
    # Monitoring
    PROMETHEUS_PORT: int = 8090
    LOG_LEVEL: str = "INFO"
    
    # Network Monitoring
    MONITORING_INTERVAL: int = 5  # seconds
    MAX_CONCURRENT_CONNECTIONS: int = 1000
    
    # Network Slicing
    MAX_SLICES_PER_TENANT: int = 10
    SLICE_SLA_CHECK_INTERVAL: int = 30  # seconds
    
    # Spectrum Analysis
    SPECTRUM_ANALYSIS_INTERVAL: int = 60  # seconds
    FREQUENCY_BANDS: List[str] = ["700MHz", "1800MHz", "2100MHz", "2600MHz", "3500MHz", "28GHz"]
    
    # RF Optimization
    RF_OPTIMIZATION_INTERVAL: int = 300  # 5 minutes
    OPTIMIZATION_ALGORITHMS: List[str] = ["genetic", "simulated_annealing", "particle_swarm"]
    
    # Capacity Planning
    CAPACITY_PREDICTION_HORIZON: int = 168  # hours (1 week)
    CAPACITY_THRESHOLD_WARNING: float = 0.8
    CAPACITY_THRESHOLD_CRITICAL: float = 0.95
    
    # InfluxDB
    INFLUXDB_URL: str = "http://localhost:8086"
    INFLUXDB_TOKEN: str = "telecom-influx-token-2024"
    INFLUXDB_ORG: str = "telecom-org"
    INFLUXDB_BUCKET: str = "network-metrics"
    
    # External APIs
    WEATHER_API_KEY: Optional[str] = None  # For RF propagation modeling
    VENDOR_API_ENDPOINTS: dict = {
        "ericsson": "https://api.ericsson.local",
        "nokia": "https://api.nokia.local",
        "samsung": "https://api.samsung.local"
    }
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()