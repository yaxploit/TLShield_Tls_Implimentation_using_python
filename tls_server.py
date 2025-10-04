#!/usr/bin/env python3
"""
TLS Secure Server Implementation
Author: Yaxploit
Description: A fully featured TLS server with mutual authentication
"""

import socket
import ssl
import threading
import os
import sys

class YaxploitTLSServer:
    """
    A secure TLS server implementation with client certificate verification
    """
    
    def __init__(self, host='localhost', port=8443):
        """
        Initialize the TLS server
        
        Args:
            host (str): Server hostname or IP address
            port (int): Server port number
        """
        self.host = host
        self.port = port
        self.context = None
        self.is_running = False
        
        # Setup SSL context and generate certificates if needed
        self.setup_ssl_context()
    
    def generate_self_signed_certificates(self):
        """
        Generate self-signed certificates for testing purposes
        
        Creates:
        - server.crt & server.key: Server certificates
        - client.crt & client.key: Client certificates for mutual TLS
        """
        print(" Generating self-signed certificates for testing...")
        
        try:
            # Generate server private key and certificate
            # -newkey rsa:2048: Generate 2048-bit RSA key
            # -days 365: Certificate valid for 1 year
            # -nodes: No DES encryption on private key
            # -x509: Create self-signed certificate
            server_cmd = (
                'openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 '
                '-subj "/C=US/ST=State/L=City/O=Yaxploit Organization/CN=localhost" '
                '-keyout server.key -out server.crt 2>/dev/null'
            )
            
            # Generate client private key and certificate
            client_cmd = (
                'openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 '
                '-subj "/C=US/ST=State/L=City/O=Yaxploit Organization/CN=client" '
                '-keyout client.key -out client.crt 2>/dev/null'
            )
            
            # Execute certificate generation commands
            os.system(server_cmd)
            os.system(client_cmd)
            
            print(" Certificates generated successfully:")
            print("  - server.crt (Server Certificate)")
            print("  - server.key (Server Private Key)")
            print("  - client.crt (Client Certificate)")
            print("  - client.key (Client Private Key)")
            
        except Exception as e:
            print(f" Error generating certificates: {e}")
            sys.exit(1)
    
    def setup_ssl_context(self):
        """
        Configure SSL context with security settings and certificates
        
        This method:
        1. Creates SSL context with TLS server protocol
        2. Sets up certificate verification
        3. Loads server certificate chain
        4. Configures secure cipher suites
        """
        try:
            # Create SSL context with TLS server protocol
            self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            
            # Require client certificate for mutual authentication
            self.context.verify_mode = ssl.CERT_REQUIRED
            
            # Generate certificates if they don't exist
            if not os.path.exists('server.crt') or not os.path.exists('server.key'):
                self.generate_self_signed_certificates()
            
            # Load server certificate and private key
            self.context.load_cert_chain('server.crt', 'server.key')
            
            # Load CA certificates to verify client certificates
            self.context.load_verify_locations('client.crt')
            
            # Configure secure cipher suites (modern, secure ciphers only)
            self.context.set_ciphers(
                'ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:'
                '!aNULL:!MD5:!DSS:!RC4:!3DES'
            )
            
            # Disable older SSL/TLS versions for security
            self.context.options |= ssl.OP_NO_SSLv2
            self.context.options |= ssl.OP_NO_SSLv3
            self.context.options |= ssl.OP_NO_TLSv1
            self.context.options |= ssl.OP_NO_TLSv1_1
            
            print(" SSL context configured successfully")
            
        except Exception as e:
            print(f" Error setting up SSL context: {e}")
            sys.exit(1)
    
    def handle_client_connection(self, conn, addr):
        """
        Handle individual client connection in a separate thread
        
        Args:
            conn (socket): Raw socket connection
            addr (tuple): Client address (ip, port)
        """
        ssl_conn = None
        try:
            print(f" New connection from {addr[0]}:{addr[1]}")
            
            # Wrap raw socket with SSL/TLS
            ssl_conn = self.context.wrap_socket(conn, server_side=True)
            
            # Get and verify client certificate
            client_cert = ssl_conn.getpeercert()
            if client_cert:
                # Extract common name from client certificate
                subject = dict(x[0] for x in client_cert['subject'])
                cn = subject.get('commonName', 'Unknown')
                print(f" Client certificate verified: {cn}")
            else:
                print(" Warning: No client certificate provided")
            
            # Send welcome message to client
            welcome_msg = f"Welcome to Yaxploit TLS Server! Connection secured.\nYour IP: {addr[0]}\n"
            ssl_conn.send(welcome_msg.encode('utf-8'))
            
            # Main communication loop
            while self.is_running:
                try:
                    # Receive data from client
                    data = ssl_conn.recv(1024)
                    if not data:
                        print(f" Client {addr[0]}:{addr[1]} disconnected")
                        break
                    
                    # Decode and process message
                    message = data.decode('utf-8').strip()
                    print(f" Received from {addr[0]}: {message}")
                    
                    # Handle quit command
                    if message.lower() == 'quit':
                        ssl_conn.send(b"Goodbye! Connection closed.\n")
                        break
                    
                    # Handle echo command
                    if message.lower().startswith('echo '):
                        response = message[5:] + "\n"
                        ssl_conn.send(response.encode('utf-8'))
                    
                    # Handle status command
                    elif message.lower() == 'status':
                        status_msg = "Server status: OK\nConnected clients: Active\n"
                        ssl_conn.send(status_msg.encode('utf-8'))
                    
                    # Handle help command
                    elif message.lower() == 'help':
                        help_msg = (
                            "Available commands:\n"
                            "  echo <message> - Echo back your message\n"
                            "  status - Check server status\n"
                            "  help - Show this help message\n"
                            "  quit - Disconnect from server\n"
                        )
                        ssl_conn.send(help_msg.encode('utf-8'))
                    
                    # Default response for unknown commands
                    else:
                        error_msg = f"Unknown command: {message}. Type 'help' for available commands.\n"
                        ssl_conn.send(error_msg.encode('utf-8'))
                        
                except ssl.SSLError as e:
                    print(f" SSL error with {addr[0]}:{addr[1]}: {e}")
                    break
                except Exception as e:
                    print(f" Error with client {addr[0]}:{addr[1]}: {e}")
                    break
                    
        except Exception as e:
            print(f" Error handling client {addr[0]}:{addr[1]}: {e}")
        finally:
            # Clean up connection
            if ssl_conn:
                try:
                    ssl_conn.close()
                except:
                    pass
            print(f" Connection with {addr[0]}:{addr[1]} closed")
    
    def start_server(self):
        """
        Start the TLS server and begin listening for connections
        """
        self.is_running = True
        
        try:
            # Create TCP socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                # Allow socket reuse
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
                # Bind to host and port
                server_socket.bind((self.host, self.port))
                
                # Listen for connections (max 10 queued connections)
                server_socket.listen(10)
                
                print(f" TLS Server started on {self.host}:{self.port}")
                print(" Waiting for client connections...")
                print(" Server is using mutual TLS authentication")
                print(" Press Ctrl+C to stop the server")
                
                # Main server loop
                while self.is_running:
                    try:
                        # Accept new client connection
                        conn, addr = server_socket.accept()
                        
                        # Handle each client in a separate thread
                        client_thread = threading.Thread(
                            target=self.handle_client_connection,
                            args=(conn, addr)
                        )
                        client_thread.daemon = True
                        client_thread.start()
                        
                    except KeyboardInterrupt:
                        print("\n Server shutdown requested...")
                        break
                    except Exception as e:
                        print(f" Error accepting connection: {e}")
                        continue
                        
        except Exception as e:
            print(f" Server error: {e}")
        finally:
            self.is_running = False
            print(" TLS Server stopped")

def main():
    """
    Main function to start the Yaxploit TLS Server
    """
    print("=" * 50)
    print(" TLS Secure Server")
    print("Author: Yaxploit")
    print("=" * 50)
    
    # Create and start server
    server = YaxploitTLSServer(host='localhost', port=8443)
    server.start_server()

if __name__ == "__main__":
    main()
