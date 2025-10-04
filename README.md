#  TLS Implementation

## 📖 Overview

A complete TLS (Transport Layer Security) client-server implementation in Python with mutual authentication. This project demonstrates secure communication using TLS protocols with certificate-based authentication.

**Author**: Yaxploit  
**Version**: 1.0  
**License**: MIT

## 🔐 What is TLS?

TLS (Transport Layer Security) is a cryptographic protocol designed to provide secure communication over a computer network. It ensures:

- **Confidentiality**: Data is encrypted and cannot be read by third parties
- **Integrity**: Data cannot be modified without detection
- **Authentication**: Both parties can verify each other's identity

### TLS Handshake Process:

1. **Client Hello**: Client sends supported TLS versions and cipher suites
2. **Server Hello**: Server selects TLS version and cipher suite
3. **Certificate Exchange**: Server sends its certificate, client may send its certificate
4. **Key Exchange**: Pre-master secret is exchanged using asymmetric cryptography
5. **Session Keys**: Both sides derive symmetric session keys from the pre-master secret
6. **Secure Communication**: Encrypted data exchange begins using symmetric encryption

## 🏗️ Project Structure

```
yaxploit-tls/
├── tls_server_yaxploit.py    # TLS Server Implementation
├── tls_client_yaxploit.py    # TLS Client Implementation
├── server.crt               # Server Certificate (auto-generated)
├── server.key               # Server Private Key (auto-generated)
├── client.crt               # Client Certificate (auto-generated)
├── client.key               # Client Private Key (auto-generated)
└── README.md               # This file
```

## ⚡ Quick Start

### Prerequisites

- Python 3.6 or higher
- OpenSSL (usually pre-installed on most systems)

### Installation

1. **Clone or download the project files**
   ```bash
   # Create project directory
   mkdir yaxploit-tls
   cd yaxploit-tls
   
   # Save the provided Python files in this directory
   ```

2. **Verify Python installation**
   ```bash
   python --version
   # Should show Python 3.6+
   ```

### Running the Implementation

#### Step 1: Start the TLS Server
```bash
python tls_server_yaxploit.py
```

**Expected Output:**
```
==================================================
Yaxploit TLS Secure Server
Author: Yaxploit
==================================================
[Yaxploit] Generating self-signed certificates for testing...
[Yaxploit] Certificates generated successfully:
  - server.crt (Server Certificate)
  - server.key (Server Private Key)
  - client.crt (Client Certificate)
  - client.key (Client Private Key)
[Yaxploit] SSL context configured successfully
[Yaxploit] TLS Server started on localhost:8443
[Yaxploit] Waiting for client connections...
[Yaxploit] Server is using mutual TLS authentication
[Yaxploit] Press Ctrl+C to stop the server
```

#### Step 2: Run the TLS Client

**Option A: Interactive Mode**
```bash
python tls_client_yaxploit.py
```

**Option B: Single Command Mode**
```bash
python tls_client_yaxploit.py "echo Hello TLS"
python tls_client_yaxploit.py status
python tls_client_yaxploit.py help
```

## 🛠️ Code Architecture

### Server Components (`tls_server_yaxploit.py`)

#### 1. **YaxploitTLSServer Class**
Main server class that handles TLS connections and client management.

#### 2. **Key Methods:**
- `generate_self_signed_certificates()`: Creates RSA certificates for testing
- `setup_ssl_context()`: Configures TLS security settings and cipher suites
- `handle_client_connection()`: Manages individual client sessions
- `start_server()`: Main server loop accepting connections

#### 3. **Security Features:**
- TLS 1.2+ only (disables older insecure versions)
- Mutual certificate authentication
- Secure cipher suites (ECDHE, AES-GCM, CHACHA20)
- 2048-bit RSA keys for certificates

### Client Components (`tls_client_yaxploit.py`)

#### 1. **YaxploitTLSClient Class**
Client class for establishing secure connections to the server.

#### 2. **Key Methods:**
- `setup_ssl_context()`: Configures client-side TLS settings
- `connect_to_server()`: Establishes secure TLS connection
- `interactive_session()`: Command-line interface for user interaction
- `single_command_mode()`: Send single commands to server

#### 3. **Operation Modes:**
- **Interactive Mode**: Real-time chat-like interface
- **Single Command Mode**: Execute one command and exit

## 🔧 Configuration

### Default Settings
- **Host**: `localhost`
- **Port**: `8443`
- **Key Size**: 2048-bit RSA
- **Certificate Validity**: 365 days

### Modifying Configuration

Edit these lines in both files to change settings:

**Server:**
```python
server = YaxploitTLSServer(host='localhost', port=8443)
```

**Client:**
```python
client = YaxploitTLSClient(host='localhost', port=8443)
```

## 📋 Available Commands

Once connected, you can use these commands:

| Command | Description | Example |
|---------|-------------|---------|
| `echo <message>` | Echo back your message | `echo Hello World` |
| `status` | Check server status | `status` |
| `help` | Show available commands | `help` |
| `quit` | Disconnect from server | `quit` |

## 🔒 Security Implementation Details

### Certificate Generation
- Automatically creates self-signed X.509 certificates
- Uses RSA 2048-bit encryption
- Certificates include organization details
- Valid for 1 year from generation

### TLS Configuration
- **Protocol**: TLSv1.2+ only
- **Cipher Suites**: ECDHE+AESGCM, ECDHE+CHACHA20, DHE+AESGCM
- **Authentication**: Mutual TLS (client and server certificates)
- **Key Exchange**: Ephemeral Diffie-Hellman for perfect forward secrecy

### Disabled for Security:
- SSLv2, SSLv3, TLSv1.0, TLSv1.1
- Weak ciphers (RC4, 3DES, MD5, DSS)
- NULL and anonymous ciphers

## 🐛 Troubleshooting

### Common Issues

1. **"Connection refused" error**
   - Ensure server is running before starting client
   - Check if port 8443 is available

2. **Certificate errors**
   - Delete existing `.crt` and `.key` files to regenerate
   - Ensure OpenSSL is installed

3. **"SSL handshake failed"**
   - Check if system time is correct
   - Verify certificates are not corrupted

4. **Port already in use**
   ```bash
   # Find process using port 8443
   lsof -i :8443
   # Kill the process if needed
   kill -9 <PID>
   ```

### Debug Mode

For detailed SSL debugging, add this to both files:
```python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

## 🔍 Testing the Implementation

### Manual Testing
1. Start server in one terminal
2. Run client in another terminal
3. Test various commands
4. Verify encrypted communication

### OpenSSL Testing
```bash
# Test server with OpenSSL client
openssl s_client -connect localhost:8443 -cert client.crt -key client.key

# Check certificate details
openssl x509 -in server.crt -text -noout
```

## 📚 Educational Value

This implementation demonstrates:

- **TLS Handshake Process**: Complete certificate exchange and key derivation
- **Socket Programming**: Raw socket manipulation with TLS wrapping
- **Threading**: Multi-client server architecture
- **Cryptography**: Certificate generation and validation
- **Network Security**: Practical implementation of security principles

## ⚠️ Important Security Notes

### For Production Use:
1. **Replace self-signed certificates** with CA-signed certificates
2. **Enable certificate validation** in client (`verify_mode = ssl.CERT_REQUIRED`)
3. **Implement proper hostname verification**
4. **Use stronger key sizes** (4096-bit RSA or ECDSA)
5. **Add certificate revocation checking**
6. **Implement proper logging and monitoring**

### Current Limitations:
- Self-signed certificates for testing only
- No certificate revocation checking
- Basic error handling for educational purposes
- No persistence or database integration

## 🎯 Use Cases

- **Educational Purposes**: Learn TLS internals and Python networking
- **Testing Environments**: Secure communication in development
- **Prototyping**: Base for more complex secure applications
- **Research**: Experiment with different TLS configurations

## 📄 License

MIT License - Feel free to use this code for educational and development purposes.

---

**Author**: Yaxploit  
**Last Updated**: 2025
