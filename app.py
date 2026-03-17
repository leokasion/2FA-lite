import io
import pyotp
import qrcode
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

@app.route('/provision/<secret>')
def provision(secret):
    """Generates a QR code in-memory (no SSD writes)."""
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name="User", issuer_name="2FA-Lite")
    
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf, 'PNG')
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png')

@app.route('/verify', methods=['POST'])
def verify():
    """API endpoint for other apps to check a code."""
    data = request.get_json()
    secret = data.get('secret')
    code = data.get('code')
    
    if not secret or not code:
        return jsonify({"error": "Missing secret or code"}), 400
        
    totp = pyotp.TOTP(secret)
    if totp.verify(code):
        return jsonify({"status": "valid"}), 200
    else:
        return jsonify({"status": "invalid"}), 401

@app.route('/health')
def health():
    """Simple health check for monitoring tools."""
    return jsonify({"status": "up"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)