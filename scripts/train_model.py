""" Training script for Iris classifier This runs ONCE to create the model file """


from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import accuracy_score
import joblib
import os


def train_and_save_model():
    print("Loading Iris dataset...")
    iris = load_iris()
    x = iris.data
    y = iris.target

    print(f"Dataset shapeL {x.shape}, Labels shape: {y.shape}")
    print(f"Classes: {iris.target_names}")

    #Split the data into train and test sets 80/20
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    print(f"Training samples: {len(x_train)}, Test Samples: {len(x_test)}")

    #train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)

    #evaluate the model
    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Test accuracy: {accuracy * 100:.2f}%")

    #save the model
    model_path = "model/iris_model.joblib"
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)

    print(f"\n✅ Model saved to {model_path}")
    print(f"File size: {os.path.getsize(model_path) / 1024:.2f} KB")
    print("\nThis file will be:")
    print("  1. Packaged in Docker image (Phase 3)")
    print("  2. Loaded by FastAPI (Phase 2)")
    print("  3. Deployed to Kubernetes (Phase 7)")




if __name__ == "__main__":
    train_and_save_model()