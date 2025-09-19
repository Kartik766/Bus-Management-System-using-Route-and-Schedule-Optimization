from flask import Flask, request, jsonify, render_template
import pandas as pd
import random
import datetime

app = Flask(__name__)

# Load the bus data to get unique routes for the frontend
try:
    bus_data = pd.read_csv('C:/Users/91775/Desktop/bms/mumbai.csv')
    unique_destinations = sorted(bus_data['Destination'].unique().tolist())
    unique_bus_names = sorted(bus_data['Bus_Name'].unique().tolist())
except FileNotFoundError:
    print("Error: mumbai.csv not found.")
    unique_destinations = []
    unique_bus_names = []

# This endpoint will be called by the frontend to get the list of routes
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/routes', methods=['GET'])
def get_routes():
    return jsonify({
        "destinations": unique_destinations,
        "bus_names": unique_bus_names
    })

# This is the core optimization endpoint
@app.route('/optimize', methods=['POST'])
def optimize_schedule():
    # The frontend sends a JSON payload with optimization parameters
    try:
        data = request.get_json()
        target_destination = data.get('destination')
        target_bus_name = data.get('bus_name')
        
        
        if not target_destination or not target_bus_name:
            return jsonify({'error': 'Destination and Bus Name are required.'}), 400

        # Simulate a dynamic schedule based on input
        num_trips = random.randint(3, 7)
        schedule = []
        start_time = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
        
        for i in range(num_trips):
            trip_start = start_time + datetime.timedelta(hours=i)
            # Simulate a variable travel time
            travel_minutes = random.randint(45, 90)
            arrival_time = trip_start + datetime.timedelta(minutes=travel_minutes)
            
            schedule.append({
                "trip_id": i + 1,
                "route": f"Mumbai to {target_destination}",
                "bus": target_bus_name,
                "departure_time": trip_start.strftime("%H:%M"),
                "arrival_time": arrival_time.strftime("%H:%M")
            })

        # Return the generated schedule as a JSON response
        return jsonify({"optimized_schedule": schedule})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)