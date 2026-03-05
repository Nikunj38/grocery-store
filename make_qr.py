import qrcode
import socket

# This part automatically finds your computer's IP address on your Wi-Fi
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

# Link to your Flask app (running on port 5000)
base_url = f"http://{get_ip()}:5000"

# Generate the QR Code
qr = qrcode.make(base_url)
qr.save("shop_qr.png")

print(f"Success! QR code created for {base_url}")
print("Look for 'shop_qr.png' in your folder.")