import numpy as np
from scipy.stats import zscore
import matplotlib.pyplot as plt
import pandas as pd


def is_ball_linear_movement(ball_data, frame_last, frame_current, std_threshold=30):
    ball_bboxes = [ball['bbox'] for ball in ball_data if frame_last <= ball['frame_number'] <= frame_current and ball['bbox'] is not None]
    df = get_centers_df(ball_bboxes)
    df_original = compute_angles(df)
    df_edited = remove_outliers(df_original)
    angle_std, x_std, y_std = calculate_std(df_edited)
    if angle_std < std_threshold or x_std < std_threshold or y_std < std_threshold:
        return True

    return False


def get_centers_df(bboxes):
    centers = [((x1 + x2) / 2, (y1 + y2) / 2) for x1, y1, x2, y2 in bboxes ]
    df = pd.DataFrame(centers, columns=["X", "Y"])
    return df


def compute_angles(df):
    dx = df["X"].diff()
    dy = df["Y"].diff()
    angles = np.degrees(np.arctan2(dy, dx))
    df["Angle"] = angles
    return df


def remove_outliers(df, threshold=2.0):
    df["Angle_Z"] = np.abs(zscore(df["Angle"].fillna(0)))  # Compute Z-score
    df["X_Z"] = np.abs(zscore(df["X"].fillna(0)))
    df["Y_Z"] = np.abs(zscore(df["Y"].fillna(0)))
    # print('Dataframe with Z-score')
    # print(df)
    df_filtered = df[(np.round(df["X_Z"]) < threshold)]
    df_filtered2 = df_filtered[np.round(df_filtered["Y_Z"]) < threshold]
    df_filtered3 = df_filtered2[np.round(df_filtered2["Angle_Z"]) < threshold]
    return df_filtered3.drop(columns=["Angle_Z", "X_Z", "Y_Z"])


def calculate_std(df):
    angle_std = np.std(df['Angle'])
    x_std = np.std(df['X'])
    y_std = np.std(df['Y'])

    return angle_std, x_std, y_std
