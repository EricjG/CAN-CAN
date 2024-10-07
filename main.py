import tkinter as tk
from tkinter import messagebox
import can
import sqlite3

class CANApp:
    def __init__(self, master):
        self.master = master
        master.title("CAN Bus Application")

        # Create a menubar
        menubar = tk.Menu(master)
        master.config(menu=menubar)

        # Create the "File" dropdown menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Project", menu=file_menu)

        # Add options under "File" for new, open, and close
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Close", command=self.close_file)

        # Add separators
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=master.quit)

        # Create the "Connection" dropdown menu
        connection_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Connection", menu=connection_menu)

        # Add options under "Connection" for connection types
        connection_menu.add_command(label="PCAN", command=lambda: self.set_connection("PCAN"))
        connection_menu.add_command(label="SocketCAN", command=lambda: self.set_connection("SocketCAN"))
        connection_menu.add_command(label="Kvaser", command=lambda: self.set_connection("Kvaser"))

        # Create a label
        self.label = tk.Label(master, text="CAN Bus Message:")
        self.label.pack()

        # Create an entry field for the message
        self.message_entry = tk.Entry(master)
        self.message_entry.pack()

        # Create a send button
        self.send_button = tk.Button(master, text="Send CAN Message", command=self.send_message)
        self.send_button.pack()

        # Create a receive button
        self.receive_button = tk.Button(master, text="Receive CAN Message", command=self.receive_message)
        self.receive_button.pack()

        # Create a text area to display received messages
        self.text_area = tk.Text(master, height=10, width=50)
        self.text_area.pack()

        # Status bar at the bottom
        self.status_var = tk.StringVar()
        self.status_var.set("Status: No connection | Sent: 0 | Received: 0")
        self.status_bar = tk.Label(master, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Default CAN bus interface (can be changed later)
        self.bus = None
        self.connection_type = None
        self.sent_packets = 0
        self.received_packets = 0

        # Initialize buttons as disabled
        self.update_buttons()

    def new_file(self):
        """Handle the creation of a new file."""
        print("New file created")

    def open_file(self):
        """Handle the opening of an existing file."""
        print("File opened")

    def close_file(self):
        """Handle the closing of the current file."""
        print("File closed")

    def set_connection(self, connection_type):
        """Sets the connection type and initializes the CAN bus"""
        self.connection_type = connection_type
        print(f"Connection type set to: {self.connection_type}")
        try:
            if connection_type == "PCAN":
                self.bus = can.interface.Bus(channel='PCAN_USBBUS1', bustype='pcan')
            elif connection_type == "SocketCAN":
                self.bus = can.interface.Bus(channel='can0', bustype='socketcan')
            elif connection_type == "Kvaser":
                self.bus = can.interface.Bus(channel=0, bustype='kvaser')

            self.update_status()
            self.update_buttons()  # Enable buttons after successful connection

        except (can.CanError, OSError) as e:
            messagebox.showerror("Connection Error", f"Unable to connect to {self.connection_type}. Please check your settings.")
            self.bus = None
            self.update_status(f"Connection Error: {self.connection_type} | Sent: {self.sent_packets} | Received: {self.received_packets}")  # Include sent and received packets
            self.update_buttons()  # Disable buttons on connection error
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
            self.bus = None
            self.update_status(f"Connection Error: {self.connection_type} | Sent: {self.sent_packets} | Received: {self.received_packets}")  # Include sent and received packets
            self.update_buttons()  # Disable buttons on unexpected error

    def send_message(self):
        message = self.message_entry.get()
        if message and self.bus:
            can_message = can.Message(arbitration_id=0x123, data=bytearray(message.encode()), is_extended_id=False)
            try:
                self.bus.send(can_message)
                self.sent_packets += 1
                self.update_status()
                print("Message sent")
            except can.CanError:
                messagebox.showerror("Send Error", "Failed to send CAN message.")
                print("Message NOT sent")
            except Exception as e:
                messagebox.showerror("Send Error", f"An error occurred while sending: {e}")

    def receive_message(self):
        if self.bus:
            try:
                msg = self.bus.recv()
                if msg:
                    self.text_area.insert(tk.END, f"Received: {msg}\n")
                    self.received_packets += 1
                    self.update_status()
            except can.CanError:
                messagebox.showerror("Receive Error", "Failed to receive CAN message.")
            except Exception as e:
                messagebox.showerror("Receive Error", f"An error occurred while receiving: {e}")

    def update_buttons(self):
        """Enables or disables buttons based on connection status."""
        if self.bus is not None:
            self.send_button.config(state=tk.NORMAL)
            self.receive_button.config(state=tk.NORMAL)
        else:
            self.send_button.config(state=tk.DISABLED)
            self.receive_button.config(state=tk.DISABLED)

    def update_status(self, custom_message=None):
        """Updates the status bar with connection info and packet counts"""
        if custom_message:
            status_text = custom_message
        else:
            status_text = (f"Status: {self.connection_type or 'No connection'} | "
                           f"Sent: {self.sent_packets} | Received: {self.received_packets}")
        self.status_var.set(status_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = CANApp(root)
    root.mainloop()
