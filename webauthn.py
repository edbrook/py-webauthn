import base64
import secrets
from flask import Flask, request

app = Flask(__name__)

USER_ID = 'sLmW8oGRXhufSA=='

def generate_challenge(size=32):
    return base64.b64encode(secrets.token_bytes(size)) \
        .decode()

@app.route('/', methods=['GET'])
def home():
    return '''
    <a id="register" href="#">Register</a>
    <br>
    <a href="/webauthn/v1/auth">Authenticate</a>
    <script>
        function convertIds(reg) {
            reg.challenge = b64ToUint8Array(reg.challenge)
            reg.user.id = b64ToUint8Array(reg.user.id)
            return reg
        }
        function b64ToUint8Array(value) {
            return Uint8Array.from(window.atob(value), c=>c.charCodeAt(0))
        }
        function register() {
            fetch('http://localhost:8080/webauthn/v1/register')
                .then(r=>r.json())
                .then(convertIds)
                .then(c => {console.log(c); return c})
                .then(publicKey => navigator.credentials.create({ publicKey }))
                .then(console.log)
                .catch(err => console.log("Error: ", err))
        }
        document.getElementById('register')
            .addEventListener('click', register)
    </script>
    '''

@app.route('/register', methods=['GET'])
def registration_challenge():
    return {
        'challenge': generate_challenge(32),
        'rp': {
            'id': 'localhost',
            'name': "localhost"
        },
        'user': {
            'id': USER_ID,
            'name': 'test-user',
            'displayName': 'test-user'
        },
        'pubKeyCredParams': [
            {'type': "public-key", 'alg': -7},
            {'type': "public-key", 'alg': -257}
        ],
        'authenticatorSelection': {
            'residentKey': 'preferred',
            'requireResidentKey': False,
            'userVerification': 'preferred'
        },
        'attestation': 'none',
        'timeout': 60000,
        'excludeCredentials': []
    }

@app.route('/auth', methods=['GET'])
def auth():
    return '''<script>
        navigator.credentials.get({
            publicKey: {
                challenge: Uint8Array.from("''' + generate_challenge(32) + '''", c => c.charCodeAt(0)),
                allowCredentials: [],
                timeout: 60000
            }
        })
        .then(res => window.pkr = res)
        .catch(console.error)
    </script>
    <a href="/webauthn/v1/">home</a>
    '''

# Example allowCredentials entry - not required
#{
#    id: Uint8Array.from("''' + USER_ID + '''", c => c.charCodeAt(0)),
#    type: 'public-key',
#    transports: ['usb', 'ble', 'nfc', 'smart-card', 'hybrid', 'internal'],
#}

