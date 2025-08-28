import sys
from bleak import *
import asyncio # used for await etc.
from aioconsole import ainput

# Based on client
NAME = "ESP_SPP_SERVER"
SERVER_UUID = "0000ABF0-0000-1000-8000-00805F9B34FB"
SERVER_WRITE_UUID = "0000ABF1-0000-1000-8000-00805F9B34FB"
SERVER_READ_UUID = "0000ABF2-0000-1000-8000-00805F9B34FB"

# first we scan for devices
class ESP32BluetoothHandler:
    def __init__(self):
        self.myDevice = []
        self.client = None
        
    # first we scan for devices
    async def scan_for_devices(self):
        for i in range(3):
            devices = await BleakScanner.discover()
            for d in devices:
                if d.name == NAME:
                    print("Found device:", d)
                    self.myDevice.append(d)
                    return self.myDevice[0]
            if not self.myDevice:
                print("Device not found, retrying in 2 secs...")
                await asyncio.sleep(2)
                
        print("Device not found after 3 attempts, exiting.")
        return None
    
    # after discovery, if we found the device, we connect to it
    async def connect(self, device):
        try:
            print("Connecting to device...")
            self.client = BleakClient(device)
            await self.client.connect() 
            
            if self.client.is_connected:
                print("Connected to device!")
                # start notify information:
                await self.client.start_notify(SERVER_READ_UUID, self.notify)
                print("Notification handler started.")
                return True
            else:
                print("Failed to connect to device.")
                return False  
        except Exception as e:
            print("Error during connection:", e)
            return False
        
    def notify(self, sender, data):
        print(f"Notification from {sender}: {data}")
        try:
            message = data.decode('utf-8')
            print(f"Received: {message}")
        except:
            print(f"Received (hex): {data.hex()}")
        
    async def read_data(self):
        try:
            if self.client and self.client.is_connected:
                data = await self.client.read_gatt_char(SERVER_READ_UUID)
                print("Read data:", data)
                return data
            else:
                print("Client is not connected.")
                return None
        except Exception as e:
            print("Error reading data:", e)
            return None
        
    async def write_data(self, data):
        try:
            if self.client and self.client.is_connected:
                await self.client.write_gatt_char(SERVER_WRITE_UUID, data)
                print("Wrote data:", data)
                return True
            else:
                print("Client is not connected.")
                return False
        except Exception as e:
            print("Error writing data:", e)
            return False
        
    async def disconnect(self):
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            print("Disconnected from device.")
            
async def main():
    client = ESP32BluetoothHandler();
    try:
        device = await client.scan_for_devices()
        if not device:
            print("Exiting program, no devices detected.")
            return
        
        if not await client.connect(device):
            print("Exiting program, connection failed.")
            return
        
        print("Connected. Read/Write ready.")
        
        while True:
            try:
                message = await ainput("Enter message to send (or 'exit' to quit): ")
                message = message.strip()
                if message.lower() == 'exit':
                    print("Exiting program.")
                    break
                else:
                    await client.write_data(message)
                    
                await asyncio.sleep(.1)  # wait a bit before next input
            except KeyboardInterrupt:
                print("Keyboard interrupt received, exiting.")
                break
            
            await client.read_data()  # read any incoming data
        
    except Exception as e:
        print("An error occurred:", e)
    finally:
        await client.disconnect()
        print("Program terminated.")
    
if __name__ == "__main__":
    asyncio.run(main())