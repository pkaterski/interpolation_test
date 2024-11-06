import pandas as pd
import numpy as np
from scipy.interpolate import CloughTocher2DInterpolator
from scipy.interpolate import LinearNDInterpolator

def create_hcl_predictor(data_csv):
    """
    Creates an interpolator for predicting HCl concentration based on temperature and density.
    
    Parameters:
    data_csv (str or pd.DataFrame): CSV data containing temperature columns and concentration rows
    
    Returns:
    CloughTocher2DInterpolator: Interpolator function that takes (temperature, density) and returns concentration
    """

    if isinstance(data_csv, str):
        df = pd.read_csv(data_csv)
    else:
        df = data_csv.copy()
    
    temp_columns = [col for col in df.columns if col != 'concentration']
    
    points = []
    values = []
    
    for temp_col in temp_columns:
        temperature = float(temp_col.replace('C', ''))
        for idx, row in df.iterrows():
            if pd.notna(row[temp_col]):
                density = row[temp_col]
                concentration = row['concentration']
                points.append([temperature, density])
                values.append(concentration)
    
    points = np.array(points)
    values = np.array(values)
    
    interpolator = CloughTocher2DInterpolator(points, values)
    #interpolator = LinearNDInterpolator(points, values)

    return interpolator

def predict_concentration(interpolator, temperature, density):
    """
    Predicts HCl concentration based on temperature and density.
    
    Parameters:
    interpolator: CloughTocher2DInterpolator object
    temperature (float): Temperature in Celsius
    density (float): Density measurement
    
    Returns:
    float: Predicted HCl concentration (w/w%)
    """
    return float(interpolator([temperature, density])[0])

if __name__ == "__main__":
    interpolator = create_hcl_predictor("data/hcl.csv")

    while True:
        print("Temperature(°C) > ", end="")
        t = float(input())
        print("Density(kg/L) > ", end="")
        d = float(input())
        c = predict_concentration(interpolator, t, d)
        print(f"concentration is {c:.4f}")

