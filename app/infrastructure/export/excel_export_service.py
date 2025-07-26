"""Excel export service for calibrated data."""

import os
from typing import Dict
import pandas as pd
from ...domain.value_objects.view_type import ViewType
from ...domain.entities.coordinate_modification import CoordinateModification


class ExcelExportService:
    """Service for exporting calibrated data to Excel files."""
    
    @staticmethod
    def export_calibrated_data(
        data_frames: Dict[str, pd.DataFrame],
        modifications: Dict[str, Dict[int, CoordinateModification]],
        output_dir: str
    ) -> Dict[str, str]:
        """Export calibrated datasets to Excel files."""
        os.makedirs(output_dir, exist_ok=True)
        written_files: Dict[str, str] = {}
        
        for view_type in ViewType:
            view_name = view_type.value
            if view_name not in data_frames:
                continue
                
            df = data_frames[view_name]
            new_df = df.copy()
            
            # Apply modifications
            view_modifications = modifications.get(view_name, {})
            for index, modification in view_modifications.items():
                if modification.is_significant():
                    x_col = view_type.get_x_column()
                    y_col = view_type.get_y_column()
                    
                    new_df.at[index, x_col] = modification.modified_coordinate.x
                    new_df.at[index, y_col] = modification.modified_coordinate.y
            
            # Write to file
            filename = f"{view_name}_calibrated.xlsx"
            path = os.path.join(output_dir, filename)
            
            try:
                new_df.to_excel(path, index=False)
                written_files[view_name] = path
            except Exception as exc:
                raise RuntimeError(f"Failed to write {view_name} data to '{path}': {exc}")
        
        return written_files
