import React, { useState, useEffect } from 'react';
import { 
  Dashboard, 
  NetworkCheck, 
  Speed, 
  Analytics 
} from '@mui/icons-material';
import { 
  Grid, 
  Card, 
  CardContent, 
  Typography, 
  Box,
  Chip,
  LinearProgress
} from '@mui/material';

function EnhancedNetworkDashboard() {
  const [networkMetrics, setNetworkMetrics] = useState({});
  const [slicePerformance, setSlicePerformance] = useState([]);
  const [anomalies, setAnomalies] = useState([]);
  
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [metricsRes, slicesRes, anomaliesRes] = await Promise.all([
          fetch('/api/v1/performance/metrics'),
          fetch('/api/v1/slicing/performance'),
          fetch('/api/v1/analytics/anomalies')
        ]);
        
        setNetworkMetrics(await metricsRes.json());
        setSlicePerformance(await slicesRes.json());
        setAnomalies(await anomaliesRes.json());
      } catch (error) {
        console.error('Dashboard data fetch failed:', error);
      }
    };
    
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 5000);
    
    return () => clearInterval(interval);
  }, []);
  
  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Typography variant='h4' gutterBottom>
        5G Network Operations Center
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display='flex' alignItems='center'>
                <NetworkCheck color='primary' sx={{ mr: 1 }} />
                <Typography variant='h6'>Network Health</Typography>
              </Box>
              <Typography variant='h3' color='primary'>
                {networkMetrics.health_score || '--'}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

export default EnhancedNetworkDashboard;
