import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Grid } from '@mui/material';
import { Line } from 'react-chartjs-2';

function NetworkSlicingDashboard() {
  const [sliceData, setSliceData] = useState([]);
  
  useEffect(() => {
    // Real-time slice monitoring
    const interval = setInterval(() => {
      fetchSliceMetrics();
    }, 5000);
    
    return () => clearInterval(interval);
  }, []);
  
  const fetchSliceMetrics = async () => {
    // Fetch from API
    const response = await fetch('/api/v1/slicing/slices');
    const data = await response.json();
    setSliceData(data.slices);
  };
  
  return (
    <Grid container spacing={3}>
      {sliceData.map(slice => (
        <Grid item xs={12} md={4} key={slice.id}>
          <Card>
            <CardContent>
              <Typography variant='h6'>{slice.type} Slice</Typography>
              <Typography>Throughput: {slice.throughput} Mbps</Typography>
              <Typography>Latency: {slice.latency} ms</Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
}

export default NetworkSlicingDashboard;
