import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
data = pd.read_csv('data.csv')

# Data preprocessing
# Fill missing values
data['fuel_type'].fillna('Unknown', inplace=True)
data.dropna(subset=['assessment_hectares'], inplace=True)

# Select features and target variables
features = ['fire_year', 'fire_location_latitude', 'fire_location_longitude', 'fuel_type']
target = 'assessment_hectares'
X = data[features]
y = data[target]

# One-hot encoding of categorical features
encoder = OneHotEncoder(sparse=False)
X_fuel_type_encoded = encoder.fit_transform(X[['fuel_type']])
fuel_type_encoded = pd.DataFrame(X_fuel_type_encoded, columns=encoder.get_feature_names_out(['fuel_type']))
X = X.drop('fuel_type', axis=1).reset_index(drop=True)
X_encoded = pd.concat([X, fuel_type_encoded], axis=1)

# Divide training set and test set
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Train a random forest regression model
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
rf_regressor.fit(X_train, y_train)

# make predictions
y_pred_train = rf_regressor.predict(X_train)
y_pred_test = rf_regressor.predict(X_test)

# Calculate MSE and R²
mse_train = mean_squared_error(y_train, y_pred_train)
mse_test = mean_squared_error(y_test, y_pred_test)
r2_train = r2_score(y_train, y_pred_train)
r2_test = r2_score(y_test, y_pred_test)

# Print evaluation results
print(f'Training MSE: {mse_train}, Testing MSE: {mse_test}')
print(f'Training R²: {r2_train}, Testing R²: {r2_test}')
