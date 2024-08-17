from flask import Flask, request, jsonify
from configs.db import get_db_connection
from constants.queries import GET_FILTERED_PRICES
from datetime import datetime

app = Flask(__name__)

@app.route('/rates', methods=['GET'])
def get_rates():
    # Get query parameters
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    if not all([date_from, date_to, origin, destination]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        date_from = datetime.strptime(date_from, '%Y-%m-%d')
        date_to = datetime.strptime(date_to, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    params = {
    "date_from": date_from,
    "date_to": date_to,
    "origin": origin,
    "destination": destination
}
    cur.execute(GET_FILTERED_PRICES, params)
    result = cur.fetchall()
    cur.close()
    conn.close()
    rates = []
    # print(result)
    for row in result:
        day_data = {
            "day": row[0].strftime('%Y-%m-%d'),
            "average_price": round(row[1]) if row[2] >= 3 else None
        }
        rates.append(day_data)
    return jsonify(rates)

if __name__ == '__main__':
    app.run(debug=True)
