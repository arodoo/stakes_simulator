"""
Data cleaning service.
Handles Excel data preprocessing and type conversion.
"""

import pandas as pd
from typing import Dict, Any


class DataCleaningService:
    """Service for cleaning and preparing Excel data for database insertion."""
    
    @staticmethod
    def clean_map_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare map table data."""
        defaults = {
            'segment': 0, 'lineDirectionTypeId': 0, 'type': 0.0, 'tid': 0.0,
            'polar': 0, 'hidenEnable': 0, 'transverse': 0.0, 'longitudinal': 0.0,
            'curvature': 0.0, 'coordinateX': 0.0, 'coordinateY': 0.0,
            'coordinateE': 0, 'coordinateN': 0, 'cruisingSpeed': 0, 'limitSpeed': 0,
            'scene': 0, 'stationType': 0.0, 'stationNum': 0, 'signallamp': 0,
            'oneWayRoad': 0, 'meetingVec': 0, 'oppositeSegment': 0
        }
        return df.fillna(defaults)
    
    @staticmethod
    def clean_centerpos2x_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare centerpos2x table data."""
        return df.fillna(0)
    
    @staticmethod
    def clean_bamboopattern_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare bamboopattern table data."""
        return df.fillna(0)
    
    @staticmethod
    def clean_largescreenpixelpos_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare largescreenpixelpos table data."""
        df = df.fillna({'stopTime': 0.0, 'residenceTime': '0'})
        for col in df.columns:
            if col not in ['residenceTime']:
                df[col] = df[col].fillna(0)
        return df
