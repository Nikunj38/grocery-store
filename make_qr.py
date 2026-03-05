import qrcode

# Your live deployed website
url = "https://grocery-store-a40t.onrender.com"

# Generate QR
qr = qrcode.make(url)

# Save QR image
qr.save("grocery_store_qr.png")

print("QR Code created successfully!")
print("Scan this QR to open:", url)