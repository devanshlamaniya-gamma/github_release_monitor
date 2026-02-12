import bcrypt

# password_string = "devansh123"

# passsword_bytes = password_string.encode("utf-8")

# salt = bcrypt.gensalt()

# hashed_password = bcrypt.hashpw(passsword_bytes , salt)

# print(password_string)
# print(hashed_password)

# stored_hash_in_db = hashed_password.decode("utf-8")
# print(stored_hash_in_db)

# login_pass = "devansh123"
# login = login_pass.encode('utf-8')

# if bcrypt.checkpw(login ,hashed_password):
#     print("yes")
# else:
#     print('no')

# password_hashing = "devansh123"
# print("password hashing",password_hashing)
# pass_bytes = password_hashing.encode("utf-8")
# print("pass bytes",pass_bytes)

# salt = bcrypt.gensalt()
# print("salt",salt)
# hashed = bcrypt.hashpw(pass_bytes , salt)
# print("hashed" , hashed)

# for_db = hashed.decode("utf-8")
# print(for_db)


# entered = "devansh123"
# entered_bit = entered.encode("utf-8")

# if bcrypt.checkpw(entered_bit , hashed):
#     print("yes")
# else:
#     print("no")

# import jwt

# paylaod_data={

#     "sub" : "4252",
#     "name" : "devansh lamaniya"

# }

# my_secret = "devansh_sceret key"

# token  = jwt.encode(
#     payload=paylaod_data,
#     key=my_secret,
#     algorithm = "HS256"
# )
# print("this is the token ..... ",token)

# import jwt

# payload = {"sub": "4252", "name": "devansh lamaniya"}
# secret = "devansh_secret_key"

# token = jwt.encode(payload, secret, algorithm="HS256")
# print("Token:", token)




# import smtplib
# from email.mime.text import MIMEText

# Email details
sender = "me@example.com"
recipient = "you@example.com"
subject = "A test email"
body = "Hi there, this is a plain text email sent from Python."

# Create a plain-text MIMEText object
# msg = MIMEText(body, 'plain') 
# msg['Subject'] = subject
# msg['From'] = sender
# msg['To'] = recipient

# Send the message via an SMTP server (example with a local server)
# try:
#     with smtplib.SMTP('localhost') as s:
#         s.send_message(msg)
#     print("Email sent successfully!")
# except ConnectionRefusedError:
#     print("Failed to connect to the SMTP server. Make sure one is running locally.")
