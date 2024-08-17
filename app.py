import logging
from flask import Flask, request, jsonify
from datetime import datetime
from configs.db import get_db_connection
from constants.queries import GET_FILTERED_PRICES

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)

@app.route('/rates', methods=['GET'])
def get_rates():
    logging.info(f"Received request with parameters: {request.args}")
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    origin = request.args.get('origin')
    destination = request.args.get('destination')


    if not all([date_from, date_to, origin, destination]):
        logging.error("Missing required parameters")
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        date_from = datetime.strptime(date_from, '%Y-%m-%d')
        date_to = datetime.strptime(date_to, '%Y-%m-%d')
        logging.info(f"Processing data from {date_from} to {date_to} for origin: {origin}, destination: {destination}")
        if date_to < date_from:
            logging.warning("Invalid date range: date_to is earlier than date_from")
            return jsonify([]) 

    except ValueError:
        logging.error("Invalid date format")
        return jsonify({"error": "Invalid date format"}), 400

 
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(GET_FILTERED_PRICES, {"date_from": date_from, "date_to": date_to, "origin": origin, "destination": destination})
        result = cur.fetchall()
        cur.close()
        conn.close()

        logging.info(f"SQL query returned {len(result)} rows")

    except Exception as e:
        logging.error(f"Database query failed: {e}")
        return jsonify({"error": "Database error"}), 500


    rates = []
    for row in result:
        day_data = {
            "day": row[0].strftime('%Y-%m-%d'),
            "average_price": row[1] if row[2] >= 3 else None #for condition where count < 3
        }
        rates.append(day_data)

    logging.info(f"Returning response with {len(rates)} entries")
    return jsonify(rates)

if __name__ == '__main__':
    app.run(debug=True)
