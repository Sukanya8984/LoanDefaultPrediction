import onnxruntime as ort
import numpy as np

# Load model
onnx_model_path = "model/svm_model.onnx"
onnx_session = ort.InferenceSession(onnx_model_path)

# Get input/output layer names
input_name = onnx_session.get_inputs()[0].name
output_name = onnx_session.get_outputs()[0].name

# Test cases (1 expected to be "Default", 0 expected to be "No Default")
test_cases = [
    [25, 30000, 15000, 600, 12, 10.5, 0.50, 36],  # Likely Default (should return 1)
    [45, 90000, 5000, 750, 120, 3.5, 0.10, 60]   # Likely No Default (should return 0)
]

# Convert to NumPy array
test_data = np.array(test_cases, dtype=np.float32)

# Run prediction
predictions = onnx_session.run([output_name], {input_name: test_data})

# Print outputs
print("Test Predictions:", predictions)
