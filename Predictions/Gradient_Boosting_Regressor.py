import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Download Data

data = pd.read_csv('data.csv')

# Handling missing values
data['fuel_type'].fillna('Unknown', inplace=True)
data.dropna(subset=['assessment_hectares'], inplace=True)

# Select features and target variables
X = data[['fire_year', 'fire_location_latitude', 'fire_location_longitude', 'fuel_type']]
y = data['assessment_hectares']

# One-hot encoding of categorical variables
encoder = OneHotEncoder(sparse=False)
X_encoded = pd.DataFrame(encoder.fit_transform(X[['fuel_type']]))
X_encoded.columns = encoder.get_feature_names_out(['fuel_type'])
X = X.drop('fuel_type', axis=1).reset_index(drop=True)
X = pd.concat([X, X_encoded], axis=1)

# Partition the data set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a gradient boosted tree model
gb_regressor = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
gb_regressor.fit(X_train, y_train)

# Forecast and evaluate
y_pred_train = gb_regressor.predict(X_train)
y_pred_test = gb_regressor.predict(X_test)
mse_train = mean_squared_error(y_train, y_pred_train)
mse_test = mean_squared_error(y_test, y_pred_test)
r2_train = r2_score(y_train, y_pred_train)
r2_test = r2_score(y_test, y_pred_test)

print(f'Train MSE: {mse_train}, Test MSE: {mse_test}')
print(f'Train R^2: {r2_train}, Test R^2: {r2_test}')
