from flask import Flask, request, jsonify
from configs.db import get_db_connection, release_db_connection,init_connection_pool
from datetime import datetime
from constants.queries import GET_FILTERED_PRICES

app = Flask(__name__)

@app.route('/rates', methods=['GET'])
def get_rates():
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    if not all([date_from, date_to, origin, destination]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        date_from = datetime.strptime(date_from, '%Y-%m-%d')
        date_to = datetime.strptime(date_to, '%Y-%m-%d')
        if date_to < date_from:
            return jsonify([])  # Return empty result for invalid date range
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(GET_FILTERED_PRICES, {"date_from": date_from, "date_to": date_to, "origin": origin, "destination": destination}) #using parameteries queries
        result = cur.fetchall()
        cur.close()

        rates = []
        for row in result: #iterating over result rows to get required json format
            day_data = {
                "day": row[0].strftime('%Y-%m-%d'),
                "average_price": int(row[1]) if row[2] >= 3 else None #when prices are >=3 return None
            }
            rates.append(day_data)
        return jsonify(rates)

    except Exception as e:
        return jsonify({"error": "Server error"}), 500

    finally:
        if conn:
            release_db_connection(conn)

if __name__ == '__main__':
    init_connection_pool()
    app.run(debug=True)
