import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from typing import Dict, List

class CapacityPlanner:
    def __init__(self):
        self.demand_model = RandomForestRegressor(n_estimators=100)
        self.capacity_thresholds = {
            'warning': 0.8,
            'critical': 0.95
        }
    
    def predict_capacity_demand(self, historical_data: pd.DataFrame, forecast_horizon: int = 168):
        '''Predict network capacity demand for next 7 days'''
        
        # Feature engineering
        features = self.extract_temporal_features(historical_data)
        X = features[['hour', 'day_of_week', 'month', 'holiday', 'weather']].values
        y = historical_data['traffic_volume'].values
        
        # Train model
        self.demand_model.fit(X, y)
        
        # Generate forecasts
        future_features = self.generate_future_features(forecast_horizon)
        predictions = self.demand_model.predict(future_features)
        
        return {
            'predictions': predictions.tolist(),
            'confidence_intervals': self.calculate_confidence_intervals(predictions),
            'capacity_alerts': self.identify_capacity_alerts(predictions)
        }
