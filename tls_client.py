#!/usr/bin/env python3
"""
TLS Secure Client Implementation
Author: Yaxploit
Description: A TLS client with certificate authentication
"""

import socket
import ssl
import sys
import os

class YaxploitTLSClient:
    """
    A secure TLS client implementation with certificate support
    """
    
    def __init__(self, host='localhost', port=8443):
        """
        Initialize the TLS client
        
        Args:
            host (str): Server hostname or IP address
            port (int): Server port number
        """
        self.host = host
        self.port = port
        self.context = None
        self.ssl_socket = None
        
        # Setup SSL context for secure connection
        self.setup_ssl_context()
    
    def setup_ssl_context(self):
        """
        Configure SSL context for client connection
        
        This method:
        1. Creates SSL context with TLS client protocol
        2. Configures certificate verification (disabled for self-signed in testing)
        3. Loads client certificates if available
        4. Sets up secure cipher suites
        """
        try:
            # Create SSL context with TLS client protocol
            self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            
            # For testing with self-signed certificates, disable hostname verification
            # In production, this should be set to True and proper CA certificates loaded
            self.context.check_hostname = False
            
            # For testing with self-signed certificates, disable certificate verification
            # In production, this should be ssl.CERT_REQUIRED with proper CA certificates
            self.context.verify_mode = ssl.CERT_NONE
            
            # Try to load client certificates for mutual authentication
            try:
                if os.path.exists('client.crt') and os.path.exists('client.key'):
                    self.context.load_cert_chain('client.crt', 'client.key')
                    print(" Client certificates loaded for mutual TLS")
                else:
                    print(" Warning: Client certificates not found. Using server-only authentication.")
            except Exception as e:
                print(f" Warning: Could not load client certificates: {e}")
            
            # Configure secure cipher suites
            self.context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS')
            
            # Disable older SSL/TLS versions
            self.context.options |= ssl.OP_NO_SSLv2
            self.context.options |= ssl.OP_NO_SSLv3
            self.context.options |= ssl.OP_NO_TLSv1
            self.context.options |= ssl.OP_NO_TLSv1_1
            
            print(" SSL context configured successfully")
            
        except Exception as e:
            print(f" Error setting up SSL context: {e}")
            sys.exit(1)
    
    def connect_to_server(self):
        """
        Establish secure TLS connection to server
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Create raw TCP socket
            raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Wrap socket with SSL/TLS
            self.ssl_socket = self.context.wrap_socket(
                raw_socket, 
                server_hostname=self.host
            )
            
            print(f" Connecting to {self.host}:{self.port}...")
            
            # Establish connection
            self.ssl_socket.connect((self.host, self.port))
            
            # Get server certificate information
            server_cert = self.ssl_socket.getpeercert()
            if server_cert:
                # Extract subject information from certificate
                subject = dict(x[0] for x in server_cert['subject'])
                organization = subject.get('organizationName', 'Unknown Organization')
                common_name = subject.get('commonName', 'Unknown')
                print(f" Connected to server: {common_name} ({organization})")
            
            # Print connection cipher information
            cipher = self.ssl_socket.cipher()
            if cipher:
                print(f" Connection secured with: {cipher[0]} ({cipher[2]} bits)")
            
            # Receive welcome message from server
            welcome_message = self.ssl_socket.recv(1024).decode('utf-8')
            print(f" Server welcome: {welcome_message}")
            
            return True
            
        except ssl.SSLError as e:
            print(f" SSL connection error: {e}")
            return False
        except ConnectionRefusedError:
            print(f" Connection refused. Is the server running on {self.host}:{self.port}?")
            return False
        except Exception as e:
            print(f" Connection error: {e}")
            return False
    
    def send_message(self, message):
        """
        Send a message to the server and receive response
        
        Args:
            message (str): Message to send to server
            
        Returns:
            str: Server response or None if error
        """
        try:
            # Send message with newline
            self.ssl_socket.send((message + '\n').encode('utf-8'))
            
            # Receive response
            response = self.ssl_socket.recv(1024).decode('utf-8')
            return response
            
        except Exception as e:
            print(f" Error sending message: {e}")
            return None
    
    def interactive_session(self):
        """
        Start interactive session with the server
        
        Provides a command-line interface for communicating with the server
        """
        print("\n Interactive session started!")
        print("Type commands to send to the server.")
        print("Available commands: echo <message>, status, help, quit")
        print("-" * 50)
        
        try:
            while True:
                # Get user input
                user_input = input("Yaxploit Client> ").strip()
                
                if not user_input:
                    continue
                
                # Send message to server
                response = self.send_message(user_input)
                
                if response:
                    print(f"Server: {response}", end='')
                
                # Check if user wants to quit
                if user_input.lower() == 'quit':
                    print(" Closing connection...")
                    break
                    
        except KeyboardInterrupt:
            print("\n Interrupted by user")
        except Exception as e:
            print(f" Session error: {e}")
        finally:
            self.disconnect()
    
    def single_command_mode(self, command):
        """
        Send a single command to server and display response
        
        Args:
            command (str): Command to send to server
        """
        print(f" Sending command: {command}")
        
        response = self.send_message(command)
        if response:
            print(f"Server response: {response}")
        else:
            print(" No response from server")
        
        self.disconnect()
    
    def disconnect(self):
        """
        Properly close the TLS connection
        """
        if self.ssl_socket:
            try:
                self.ssl_socket.close()
                print(" Disconnected from server")
            except Exception as e:
                print(f" Error closing connection: {e}")
        else:
            print(" No active connection to close")

def display_usage():
    """
    Display usage information for the client
    """
    print("Usage:")
    print("  python tls_client_yaxploit.py                    # Interactive mode")
    print("  python tls_client_yaxploit.py <command>          # Single command mode")
    print("\nExamples:")
    print("  python tls_client_yaxploit.py")
    print("  python tls_client_yaxploit.py \"echo Hello World\"")
    print("  python tls_client_yaxploit.py status")
    print("  python tls_client_yaxploit.py help")

def main():
    """
    Main function to run the Yaxploit TLS Client
    """
    print("=" * 50)
    print("Yaxploit TLS Secure Client")
    print("Author: Yaxploit")
    print("=" * 50)
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        # Check for help flag
        if sys.argv[1] in ['-h', '--help', 'help']:
            display_usage()
            return
        
        # Single command mode
        command = ' '.join(sys.argv[1:])
        client = YaxploitTLSClient(host='localhost', port=8443)
        
        if client.connect_to_server():
            client.single_command_mode(command)
        else:
            print(" Failed to connect to server")
    
    else:
        # Interactive mode
        client = YaxploitTLSClient(host='localhost', port=8443)
        
        if client.connect_to_server():
            client.interactive_session()
        else:
            print("Failed to connect to server")

if __name__ == "__main__":
    main()
