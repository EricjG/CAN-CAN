import tkinter as tk
import can  # Ensure you have the python-can library installed

class CANApp:
    def __init__(self, master):
        self.master = master
        master.title("CAN Bus Application")

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

        # Set up CAN interface
        self.bus = can.interface.Bus(channel='can0', bustype='socketcan')  # Modify as needed

    def send_message(self):
        message = self.message_entry.get()
        if message:
            # Create a CAN message
            can_message = can.Message(arbitration_id=0x123, data=bytearray(message.encode()), is_extended_id=False)
            try:
                self.bus.send(can_message)
                print("Message sent")
            except can.CanError:
                print("Message NOT sent")

    def receive_message(self):
        try:
            msg = self.bus.recv()  # Blocking call, waits for a CAN message
            if msg:
                self.text_area.insert(tk.END, f"Received: {msg}\n")
                print(f"Received: {msg}")
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = CANApp(root)
    root.mainloop()
