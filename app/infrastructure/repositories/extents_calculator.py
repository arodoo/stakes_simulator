"""Extents calculation utilities."""

import pandas as pd
from typing import Dict
from ...domain.value_objects.view_type import ViewType
from ...domain.value_objects.extents import Extents


class ExtentsCalculator:
    """Calculates coordinate extents for views."""
    
    def compute_all_extents(self, data_frames: Dict[str, pd.DataFrame]) -> Dict[str, Extents]:
        """Compute extents for all view types."""
        extents = {}
        
        for view_type in ViewType:
            view_key = view_type.value
            if view_key not in data_frames:
                continue
                
            df = data_frames[view_key]
            x_col = view_type.get_x_column()
            y_col = view_type.get_y_column()
            
            if x_col not in df.columns or y_col not in df.columns:
                raise ValueError(f"Missing {x_col}/{y_col} columns in {view_key}")
            
            min_x, max_x = df[x_col].min(), df[x_col].max()
            min_y, max_y = df[y_col].min(), df[y_col].max()
            
            # Ensure min <= max for both axes  
            if min_x > max_x:
                min_x, max_x = max_x, min_x
            if min_y > max_y:
                min_y, max_y = max_y, min_y
            
            extents[view_key] = Extents(min_x, max_x, min_y, max_y)
        
        return extents
