import tkinter as tk
import can
import ctypes

class CANApp:
    def __init__(self, master):
        self.master = master
        master.title("CAN Bus Application")

        # Dropdown label
        self.label = tk.Label(master, text="Select CAN Interface:")
        self.label.pack()

        # Dropdown for CAN interface
        self.interfaces = self.get_available_can_interfaces()  # Get available CAN interfaces
        self.selected_interface = tk.StringVar(master)
        self.selected_interface.set(self.interfaces[0] if self.interfaces else "No interfaces found")
        self.interface_menu = tk.OptionMenu(master, self.selected_interface, *self.interfaces)
        self.interface_menu.pack()

        # Send and Receive Message Areas
        self.send_label = tk.Label(master, text="Message to Send:")
        self.send_label.pack()
        
        self.message_entry = tk.Entry(master)
        self.message_entry.pack()

        self.receive_label = tk.Label(master, text="Received Messages:")
        self.receive_label.pack()

        self.text_area = tk.Text(master, height=10, width=50)
        self.text_area.pack()

        # Buttons for sending and receiving messages
        self.send_button = tk.Button(master, text="Send CAN Message", command=self.send_message)
        self.send_button.pack()

        self.receive_button = tk.Button(master, text="Receive CAN Message", command=self.receive_message)
        self.receive_button.pack()

        # Initialize CAN bus connection (empty at first)
        self.bus = None

    def get_available_can_interfaces(self):
        """
        Get the available CAN interfaces on the system.
        Currently just hardcoded for demonstration. This can be expanded 
        to check for specific hardware dynamically (e.g., Kvaser, PCAN).
        """
        interfaces = []
        try:
            # Example for Kvaser - Check if the DLL can be loaded
            canlib = ctypes.windll.LoadLibrary("canlib32.dll")
            channels = ctypes.c_int()
            status = canlib.canGetNumberOfChannels(ctypes.byref(channels))
            if status == 0:
                for i in range(channels.value):
                    interfaces.append(f"Kvaser channel {i}")
        except Exception:
            pass
        
        # Hardcoded interface options - replace this with actual detection logic
        interfaces.extend(["PCAN_USBBUS1", "Kvaser 0", "Virtual CAN"])
        
        if not interfaces:
            interfaces.append("No interfaces found")
        
        return interfaces

    def send_message(self):
        selected_interface = self.selected_interface.get()
        if selected_interface and self.message_entry.get():
            try:
                if not self.bus:
                    self.bus = self.setup_can_bus(selected_interface)
                can_message = can.Message(arbitration_id=0x123, data=bytearray(self.message_entry.get().encode()), is_extended_id=False)
                self.bus.send(can_message)
                self.text_area.insert(tk.END, "Message sent!\n")
            except Exception as e:
                self.text_area.insert(tk.END, f"Failed to send message: {e}\n")
        else:
            self.text_area.insert(tk.END, "No message to send or no CAN interface selected.\n")

    def receive_message(self):
        selected_interface = self.selected_interface.get()
        if selected_interface:
            try:
                if not self.bus:
                    self.bus = self.setup_can_bus(selected_interface)
                msg = self.bus.recv(timeout=1.0)  # Wait 1 second for a message
                if msg:
                    self.text_area.insert(tk.END, f"Received message: {msg}\n")
                else:
                    self.text_area.insert(tk.END, "No message received.\n")
            except Exception as e:
                self.text_area.insert(tk.END, f"Failed to receive message: {e}\n")
        else:
            self.text_area.insert(tk.END, "No CAN interface selected.\n")

    def setup_can_bus(self, interface_name):
        """
        Set up the CAN bus connection based on the selected interface.
        Modify this function based on the actual hardware you use.
        """
        try:
            if "PCAN" in interface_name:
                return can.interface.Bus(channel='PCAN_USBBUS1', interface='pcan')
            elif "Kvaser" in interface_name:
                return can.interface.Bus(channel=0, interface='kvaser')
            elif "Virtual" in interface_name:
                return can.interface.Bus(channel='vcan0', interface='socketcan')
            else:
                raise ValueError(f"Unknown interface: {interface_name}")
        except Exception as e:
            self.text_area.insert(tk.END, f"Error setting up CAN bus: {e}\n")
            raise

if __name__ == "__main__":
    root = tk.Tk()
    app = CANApp(root)
    root.mainloop()
