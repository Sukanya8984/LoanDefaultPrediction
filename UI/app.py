from flask import Flask, render_template, request, jsonify
import mysql.connector
import onnxruntime as ort
import numpy as np
import os

# Initialize Flask app
app = Flask(__name__, template_folder="templates")  # Ensure templates folder is set

# MySQL Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",  # Change if needed
    "password": "ishika2802",  # Enter your MySQL Workbench password
    "database": "LoanPredictionDB"
}

# Connect to MySQL
def connect_db():
    try:
        conn = mysql.connector.connect(**db_config)
        print("✅ Database Connection Successful!")
        return conn
    except mysql.connector.Error as err:
        print(f"🚨 Database Connection Failed: {err}")
        return None
    
# Load the ONNX model
onnx_model_path = "model\svm_model.onnx"
onnx_session = ort.InferenceSession(onnx_model_path)

# Get the name of the input and output layer
input_name = onnx_session.get_inputs()[0].name  # Input layer name
output_name = onnx_session.get_outputs()[0].name  # Output layer name

@app.route("/")
def home():
    print("Templates found:", os.listdir("templates/"))  # Debugging output
    return render_template("index.html")  # Ensure index.html is inside /templates/

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get input data from JSON request
        data = request.get_json()

        # Convert input features to NumPy array
        #input_features = np.array([data["features"]], dtype=np.float32)  # Ensure it's 2D
        input_features = np.array([[data["age"], data["income"], data["loanAmount"], 
                                    data["creditScore"], data["monthsEmployed"], 
                                    data["interestRate"], data["dtiRatio"], data["loanTerm"]]], 
                                  dtype=np.float32)
        
        # Make prediction using ONNX model
        prediction = onnx_session.run([output_name], {input_name: input_features})

        # Print the raw output to debug
        print("Raw Prediction Output:", prediction)

        # Extract the first value from the prediction array
        predicted_value = int(prediction[0][0])  # Get scalar value

        # Print to verify prediction
        print("Predicted Value (After Conversion):", predicted_value)
        
        # Determine result message
        result_message = "❌ You cannot apply for the loan." if predicted_value == 1 else "✅ You can apply for the loan."

        # Store data in MySQL
        conn = connect_db()
        cursor = conn.cursor()
        sql = """
        INSERT INTO loan_applications (age, income, loanAmount, creditScore, monthsEmployed, interestRate, dtiRatio, loanTerm, prediction)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (data["age"], data["income"], data["loanAmount"], 
              data["creditScore"], data["monthsEmployed"], 
              data["interestRate"], data["dtiRatio"], data["loanTerm"], predicted_value)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()

        # Return prediction result
        return jsonify({"prediction": int(predicted_value), "message": result_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
