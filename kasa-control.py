import asyncio
from kasa import Discover
import sys

async def find_devices():
    """Scan and find all Kasa devices on the local network."""
    try:
        devices = await Discover.discover()
        return devices
    except Exception as e:
        print(f"Error discovering devices: {e}")
        return {}

async def power_cycle(device):
    """Turn device off, wait 1 second, then turn it back on."""
    try:
        print("Power cycling device...")
        await device.turn_off()
        await asyncio.sleep(1)
        await device.turn_on()
        print("Power cycle complete")
    except Exception as e:
        print(f"Error during power cycle: {e}")

async def control_device(device):
    """Control the selected device's power state."""
    try:
        # Update device info
        await device.update()
        
        # Show current state
        state = "ON" if device.is_on else "OFF"
        print(f"\nCurrent device state: {state}")
        
        # Show menu
        print("\nAvailable actions:")
        print("1. Turn ON")
        print("2. Turn OFF")
        print("3. Power Cycle (off then on after 1 second)")
        
        # Get user input for desired state
        while True:
            try:
                action = int(input("\nEnter your choice (1-3): "))
                if 1 <= action <= 3:
                    break
                print("Please enter a number between 1 and 3")
            except ValueError:
                print("Please enter a valid number")
        
        # Execute the action
        if action == 1:
            await device.turn_on()
            print("Device turned ON")
        elif action == 2:
            await device.turn_off()
            print("Device turned OFF")
        else:  # action == 3
            await power_cycle(device)
            
    except Exception as e:
        print(f"Error controlling device: {e}")

async def main():
    print("Scanning for Kasa devices on your network...")
    devices = await find_devices()
    
    if not devices:
        print("No devices found. Please ensure devices are connected to your network.")
        return
    
    # Create a numbered list of devices
    device_list = list(devices.values())
    print("\nFound devices:")
    for i, device in enumerate(device_list, 1):
        await device.update()
        state = "ON" if device.is_on else "OFF"
        print(f"{i}. {device.alias} ({device.model}) - Currently {state}")
    
    # Get user selection
    while True:
        try:
            selection = int(input("\nSelect a device number to control: "))
            if 1 <= selection <= len(device_list):
                break
            print(f"Please enter a number between 1 and {len(device_list)}")
        except ValueError:
            print("Please enter a valid number")
    
    selected_device = device_list[selection - 1]
    print(f"\nSelected device: {selected_device.alias}")
    
    await control_device(selected_device)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
        sys.exit(0)
