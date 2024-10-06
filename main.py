import tkinter as tk
import can

class CANApp:
    def __init__(self, master):
        self.master = master
        master.title("CAN Bus Application")

        self.label = tk.Label(master, text="CAN Bus Message:")
        self.label.pack()

        self.message_entry = tk.Entry(master)
        self.message_entry.pack()

        self.send_button = tk.Button(master, text="Send CAN Message", command=self.send_message)
        self.send_button.pack()

        self.receive_button = tk.Button(master, text="Receive CAN Message", command=self.receive_message)
        self.receive_button.pack()

        self.text_area = tk.Text(master, height=10, width=50)
        self.text_area.pack()

        # Set up CAN interface
        self.bus = self.setup_can_interface()

    def setup_can_interface(self):
        """
        Try multiple CAN interfaces and return the first successful one.
        """
        bus_interfaces = [
            ('PCAN_USBBUS1', 'pcan'),  # PCAN example
            (0, 'kvaser'),             # Kvaser example
            ('can0', 'socketcan'),      # SocketCAN for Linux
            # Add other interfaces as needed
        ]
        
        for channel, interface in bus_interfaces:
            try:
                bus = can.interface.Bus(channel=channel, interface=interface)  # Updated to use 'interface'
                self.text_area.insert(tk.END, f"Connected to CAN interface: {interface}\n")
                print(f"Connected to CAN interface: {interface}")
                return bus
            except OSError as e:
                self.text_area.insert(tk.END, f"Failed to connect to {interface}: {e}\n")
                print(f"Failed to connect to {interface}: {e}")
        
        # If no connection could be established, return None
        self.text_area.insert(tk.END, "No CAN interfaces found. Please check your hardware.\n")
        print("No CAN interfaces found. Please check your hardware.")
        return None

    def send_message(self):
        if self.bus:
            message = self.message_entry.get()
            if message:
                can_message = can.Message(arbitration_id=0x123, data=bytearray(message.encode()), is_extended_id=False)
                try:
                    self.bus.send(can_message)
                    self.text_area.insert(tk.END, "Message sent\n")
                    print("Message sent")
                except can.CanError:
                    self.text_area.insert(tk.END, "Message NOT sent\n")
                    print("Message NOT sent")
        else:
            self.text_area.insert(tk.END, "No CAN interface available. Cannot send message.\n")

    def receive_message(self):
        if self.bus:
            try:
                msg = self.bus.recv(timeout=1.0)  # Wait for 1 second for a message
                if msg:
                    self.text_area.insert(tk.END, f"Received: {msg}\n")
                    print(f"Received: {msg}")
                else:
                    self.text_area.insert(tk.END, "No message received.\n")
            except can.CanError as e:
                self.text_area.insert(tk.END, f"Error receiving message: {e}\n")
                print(f"Error receiving message: {e}")
        else:
            self.text_area.insert(tk.END, "No CAN interface available. Cannot receive messages.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = CANApp(root)
    root.mainloop()
