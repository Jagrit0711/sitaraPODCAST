from sklearn.tree import DecisionTreeClassifier
import numpy as np

class StarPredictor:
    def __init__(self):
        self.model = DecisionTreeClassifier(random_state=42)
        self.initialize_model()
        
    def initialize_model(self):
        # Generate training data based on astronomical principles
        masses = np.linspace(8, 50, 100)  # Stars from 8 to 50 solar masses
        metallicities = np.random.uniform(0.005, 0.02, 100)  # Typical metallicity ranges
        
        # Prepare features
        X = np.column_stack([masses, metallicities])
        
        # Generate labels (0: Neutron Star, 1: Black Hole)
        # Stars above ~25 solar masses typically form black holes
        y = (masses > 25).astype(int)
        
        # Train the model
        self.model.fit(X, y)
        
    def predict_final_stage(self, mass, metallicity=0.02):
        # Input validation
        if mass < 8:
            return "White Dwarf"  # Stars below 8 solar masses
        
        # Prepare input for prediction
        features = np.array([[mass, metallicity]])
        prediction = self.model.predict(features)[0]
        
        # Get prediction probability
        prob = self.model.predict_proba(features)[0]
        confidence = max(prob) * 100
        
        result = "Black Hole" if prediction == 1 else "Neutron Star"
        return {
            'final_stage': result,
            'confidence': confidence,
            'probability': {
                'neutron_star': prob[0] * 100,
                'black_hole': prob[1] * 100
            }
        }