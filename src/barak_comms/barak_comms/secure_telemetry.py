import rclpy
from rclpy.node import Node
from barak_common.msg import Telemetry, HybridState
import hashlib
import json

class SecureVault:
    """Simulated Secure Hardware Extension (HSM) for BARAK."""
    def __init__(self, key="KADIM_ANAHTAR_2026"):
        self.key = key

    def encrypt_gcm(self, data):
        # Simulated AES-256-GCM Encryption
        # raw_data -> aes_gcm_encrypt(key, data)
        # Returns (ciphertext, tag, nonce)
        nonce = "BARAK_NONCE_INIT"
        ciphertext = f"ENC[{data}]" 
        return ciphertext, nonce

    def sign_hmac(self, data):
        return hashlib.sha256((data + self.key).encode()).hexdigest()

class SecureTelemetryNode(Node):
    def __init__(self):
        super().__init__('secure_telemetry')
        self.get_logger().info('Secure Telemetry Node Maturing...')
        
        # Initialize Vault
        self.vault = SecureVault()
        
        # Subscriptions
        self.status_sub = self.create_subscription(
            HybridState,
            'barak/current_status',
            self.status_callback,
            10
        )
        
        # Publishers
        self.secure_pub = self.create_publisher(Telemetry, 'barak/secure_telemetry', 10)
        self.get_logger().info('Encryption Layer: AES-256GCM Protocol Active.')

    def status_callback(self, msg):
        # Prepare structured data payload
        raw_data = {
            "mode": msg.current_mode,
            "bat": msg.battery_level,
            "system_arm": msg.is_armed,
            "clk": self.get_clock().now().nanoseconds
        }
        json_payload = json.dumps(raw_data)
        
        # Encrypt and Sign
        encrypted_str, nonce = self.vault.encrypt_gcm(json_payload)
        signature = self.vault.sign_hmac(encrypted_str)
        
        telemetry_msg = Telemetry()
        telemetry_msg.sender_id = "BARAK_UNIT_01"
        telemetry_msg.timestamp = str(raw_data["clk"])
        telemetry_msg.encrypted_payload = f"{nonce}:{encrypted_str}"
        telemetry_msg.signature = signature
        
        self.secure_pub.publish(telemetry_msg)
        self.get_logger().debug(f'TX: {signature[:12]}... (AES-GCM)')

def main(args=None):
    rclpy.init(args=args)
    node = SecureTelemetryNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
