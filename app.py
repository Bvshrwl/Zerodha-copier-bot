
from flask import Flask, request, jsonify
import os
import pyotp
from kiteconnect import KiteConnect

app = Flask(__name__)

kite = KiteConnect(api_key=os.getenv("Z_API_KEY"))

@app.route('/entry', methods=['POST'])
def entry():
    data = request.json
    action = data.get("action")
    symbol = data.get("symbol")
    qty = data.get("qty")
    slave_tokens = os.getenv("SLAVE_TOKENS", "").split(",")
    results = []
    for token in slave_tokens:
        kite.set_access_token(token.strip())
        try:
            order = kite.place_order(
                variety=kite.VARIETY_REGULAR,
                exchange="NSE",
                tradingsymbol=symbol,
                transaction_type=kite.TRANSACTION_TYPE_BUY if action == "buy" else kite.TRANSACTION_TYPE_SELL,
                quantity=int(qty),
                product=kite.PRODUCT_MIS,
                order_type=kite.ORDER_TYPE_MARKET
            )
            results.append({ "token": token, "order_id": order })
        except Exception as e:
            results.append({ "token": token, "error": str(e) })
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
