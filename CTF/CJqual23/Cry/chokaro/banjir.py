import qrcode
from pyzbar.pyzbar import decode

# Assuming you have created a QR code using the provided code
# FLAG = "Hello, QR Code!"
# qr = qrcode.QRCode(border=0)
# qr.add_data(FLAG)
# qr.make(fit=True)

# # Get the matrix representation of the QR code
# matrix = qr.get_matrix()

# # Save the matrix as an image for demonstration purposes
# image_path = 'qr_matrix.png'
# qrcode.make(matrix).save(image_path)

# # Decode the content from the image using pyzbar
# decoded_objects = decode(qrcode.make(matrix))

# # Display the decoded information
# for obj in decoded_objects:
#     print(f'Data: {obj.data.decode("utf-8")}')
#     print(f'Type: {obj.type}')
#     print(f'Position: {obj.polygon}\n')


a = open("mixed.png", "rb").read()

print(a.count(b"\x89"))

# for b in a[:32]:

#     co = a.count(bytes([b]))
#     if co < 3:
#         print(bytes([b]), co)