# Deployment Manual

## Overview

This manual covers production deployment of Telecom Network Wrangler in carrier-grade environments.

## System Requirements

### Minimum Hardware
- **CPU**: 8 cores (Intel Xeon or AMD EPYC)
- **RAM**: 32 GB
- **Storage**: 500 GB SSD (database and logs)
- **Network**: 1 Gbps management interface

### Recommended Hardware
- **CPU**: 16+ cores with hyperthreading
- **RAM**: 64+ GB
- **Storage**: 1 TB NVMe SSD (high IOPS required)
- **Network**: 10 Gbps bonded interfaces

### Software Dependencies
- **OS**: Ubuntu 22.04 LTS or RHEL 8+
- **Container Runtime**: Docker 24+ or Podman 4+
- **Database**: PostgreSQL 15+ with TimescaleDB
- **Cache**: Redis 7+
- **Monitoring**: Prometheus + Grafana

## Production Deployment

### 1. Infrastructure Preparation

#### Database Setup
```bash
# PostgreSQL with TimescaleDB
sudo apt install postgresql-15 postgresql-15-repackage
wget https://packagecloud.io/install/repositories/timescale/timescaledb/script.deb.sh
sudo bash script.deb.sh
sudo apt install timescaledb-2-postgresql-15

# Initialize database
sudo -u postgres createdb network_wrangler
sudo -u postgres psql network_wrangler -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"
```

#### Docker Swarm Setup
```bash
# Initialize swarm mode
docker swarm init --advertise-addr <MANAGER_IP>

# Add worker nodes
docker swarm join --token <TOKEN> <MANAGER_IP>:2377
```

### 2. Configuration Management

#### Environment Variables
```bash
# Production environment file
cat > .env.production << EOF
DATABASE_URL=postgresql://user:pass@db:5432/network_wrangler
REDIS_URL=redis://redis:6379/0
API_PORT=8080
LOG_LEVEL=INFO
ENVIRONMENT=production
SECRET_KEY=<generate-secure-key>
JWT_SECRET=<generate-jwt-secret>
SNMP_COMMUNITY=<production-community>
EOF
```

#### Docker Compose Production
```yaml
version: '3.8'
services:
  api:
    image: telecom-network-wrangler:latest
    deploy:
      replicas: 3
      placement:
        constraints:
          - node.role == worker
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    networks:
      - backend
    
  database:
    image: timescale/timescaledb:latest-pg15
    deploy:
      placement:
        constraints:
          - node.role == manager
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: network_wrangler
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    
  redis:
    image: redis:7-alpine
    deploy:
      replicas: 1
    volumes:
      - redis_data:/data

volumes:
  db_data:
  redis_data:

networks:
  backend:
    driver: overlay
```

### 3. Security Configuration

#### TLS/SSL Setup
```bash
# Generate certificates
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout server.key -out server.crt \
  -subj "/C=US/ST=CA/L=SF/O=Telecom/CN=network-wrangler.local"

# Configure nginx reverse proxy
cat > nginx.conf << EOF
server {
    listen 443 ssl;
    server_name network-wrangler.local;
    
    ssl_certificate /etc/ssl/server.crt;
    ssl_certificate_key /etc/ssl/server.key;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF
```

#### Firewall Rules
```bash
# Allow only necessary ports
ufw allow 22    # SSH
ufw allow 443   # HTTPS
ufw allow 161   # SNMP
ufw deny 8080   # Block direct API access
ufw enable
```

### 4. Monitoring Setup

#### Prometheus Configuration
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'network-wrangler'
    static_configs:
      - targets: ['api:8080']
    metrics_path: '/metrics'
    
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
```

#### Grafana Dashboards
- Network health overview
- Performance metrics
- SLA compliance tracking
- Alert status dashboard

### 5. Backup and Recovery

#### Database Backup
```bash
# Daily backup script
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)

pg_dump -h localhost -U postgres network_wrangler | \
  gzip > "$BACKUP_DIR/network_wrangler_$DATE.sql.gz"

# Retain last 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

#### Disaster Recovery
1. Maintain offsite backup copies
2. Document recovery procedures
3. Test recovery quarterly
4. Maintain standby database

### 6. Performance Tuning

#### PostgreSQL Optimization
```sql
-- Optimize for time-series workload
ALTER SYSTEM SET shared_buffers = '16GB';
ALTER SYSTEM SET effective_cache_size = '48GB';
ALTER SYSTEM SET work_mem = '256MB';
ALTER SYSTEM SET max_worker_processes = 16;
ALTER SYSTEM SET max_parallel_workers = 16;
SELECT pg_reload_conf();
```

#### Application Tuning
```python
# Connection pooling
DATABASE_CONFIG = {
    'pool_size': 20,
    'max_overflow': 30,
    'pool_timeout': 30,
    'pool_recycle': 3600
}

# Redis optimization
REDIS_CONFIG = {
    'maxmemory': '8gb',
    'maxmemory_policy': 'allkeys-lru'
}
```

### 7. Health Checks

#### Application Health
```bash
# Health check endpoint
curl -f http://localhost:8080/health || exit 1

# Database connectivity
pg_isready -h localhost -p 5432 -U postgres

# Redis connectivity  
redis-cli ping
```

#### Monitoring Alerts
- API response time > 500ms
- Database connection failures
- Memory usage > 80%
- Disk space < 20%
- Network element polling failures

### 8. Scaling Guidelines

#### Horizontal Scaling
- Add worker nodes to Docker Swarm
- Increase API service replicas
- Implement database read replicas
- Use load balancer for API traffic

#### Vertical Scaling
- Monitor resource utilization
- Scale CPU/Memory based on load
- Optimize database queries
- Implement caching strategies

## Production Checklist

### Pre-deployment
- [ ] Hardware requirements verified
- [ ] Network connectivity tested
- [ ] Security certificates installed
- [ ] Database initialized and optimized
- [ ] Backup procedures configured
- [ ] Monitoring dashboards ready

### Post-deployment
- [ ] Health checks passing
- [ ] Performance metrics baseline established
- [ ] Alerts configured and tested
- [ ] Documentation updated
- [ ] Team training completed
- [ ] Incident response procedures verified

## Troubleshooting

### Common Issues

#### High Memory Usage
- Check for memory leaks in application logs
- Monitor database connection pools
- Review caching configuration

#### Slow API Response
- Check database query performance
- Monitor network latency
- Review indexing strategy

#### Data Loss Prevention
- Verify backup procedures
- Test recovery processes
- Monitor disk space
- Implement data retention policies

## Support

For deployment assistance:
- Internal documentation: `/docs`
- Technical support: operations@company.com
- Emergency escalation: +1-800-SUPPORT