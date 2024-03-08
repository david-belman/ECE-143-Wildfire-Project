import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
data = pd.read_csv('data.csv')

# Basic preprocessing - Selecting numerical features for simplicity. Adjust as necessary.
# Assuming 'assessment_hectares' is the target for the size of the fire
features = data.select_dtypes(include=['float64', 'int64']).columns.drop('assessment_hectares')
X = data[features].fillna(0)  # Simple NA fill-in for demonstration
y = data['assessment_hectares'].fillna(0)  # Ensure no NA values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features by removing the mean and scaling to unit variance
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize and train the SVM model
svr_model = SVR()
svr_model.fit(X_train_scaled, y_train)

# Make predictions
y_train_pred = svr_model.predict(X_train_scaled)
y_test_pred = svr_model.predict(X_test_scaled)

# Evaluate the model
train_mse = mean_squared_error(y_train, y_train_pred)
test_mse = mean_squared_error(y_test, y_test_pred)
train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)

print(f'Training MSE: {train_mse}, Testing MSE: {test_mse}')
print(f'Training R²: {train_r2}, Testing R²: {test_r2}')
