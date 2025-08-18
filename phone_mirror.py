#!/usr/bin/env python3
"""
Minimal scrcpy script for Android phone mirroring and control via ADB.
No UI, no interface, no design elements - just pure mirroring and control.
"""

import subprocess
import sys
import os
import time
from typing import Optional, List


class PhoneMirror:
    def __init__(self):
        self.device_id: Optional[str] = None
        self.scrcpy_process: Optional[subprocess.Popen] = None
    
    def check_adb_installed(self) -> bool:
        """Check if ADB is installed and accessible."""
        try:
            result = subprocess.run(['adb', 'version'], 
                                  capture_output=True, text=True, check=True)
            print(f"ADB found: {result.stdout.splitlines()[0]}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: ADB not found. Please install Android SDK Platform Tools.")
            return False
    
    def check_scrcpy_installed(self) -> bool:
        """Check if scrcpy is installed and accessible."""
        # First check if scrcpy is in the current directory
        local_scrcpy = os.path.join(os.getcwd(), 'scrcpy.exe')
        if os.path.exists(local_scrcpy):
            print(f"scrcpy found (local): {local_scrcpy}")
            return True
        
        # Then check if scrcpy is in PATH
        try:
            result = subprocess.run(['scrcpy', '--version'], 
                                  capture_output=True, text=True, check=True)
            print(f"scrcpy found (PATH): {result.stdout.splitlines()[0]}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: scrcpy not found. Please install scrcpy.")
            print("Run: install_scrcpy.bat")
            print("Or download from: https://github.com/Genymobile/scrcpy")
            return False
    
    def get_connected_devices(self) -> List[str]:
        """Get list of connected Android devices."""
        try:
            result = subprocess.run(['adb', 'devices'], 
                                  capture_output=True, text=True, check=True)
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            devices = []
            for line in lines:
                if line.strip() and '\tdevice' in line:
                    device_id = line.split('\t')[0]
                    devices.append(device_id)
            return devices
        except subprocess.CalledProcessError as e:
            print(f"Error getting devices: {e}")
            return []
    
    def select_device(self) -> Optional[str]:
        """Select a device to connect to."""
        devices = self.get_connected_devices()
        
        if not devices:
            print("No Android devices found.")
            print("Please:")
            print("1. Enable USB debugging on your phone")
            print("2. Connect your phone via USB")
            print("3. Allow USB debugging when prompted on your phone")
            return None
        
        if len(devices) == 1:
            device_id = devices[0]
            print(f"Found device: {device_id}")
            return device_id
        
        print("Multiple devices found:")
        for i, device_id in enumerate(devices, 1):
            print(f"{i}. {device_id}")
        
        try:
            choice = int(input("Select device (number): ")) - 1
            if 0 <= choice < len(devices):
                return devices[choice]
            else:
                print("Invalid selection.")
                return None
        except ValueError:
            print("Invalid input.")
            return None
    
    def start_mirroring(self, device_id: str) -> bool:
        """Start scrcpy mirroring for the specified device."""
        try:
            # Determine scrcpy executable path
            local_scrcpy = os.path.join(os.getcwd(), 'scrcpy.exe')
            if os.path.exists(local_scrcpy):
                scrcpy_exe = local_scrcpy
            else:
                scrcpy_exe = 'scrcpy'
            
            # Basic scrcpy command with minimal options
            cmd = [
                scrcpy_exe,
                '--serial', device_id,
                '--no-audio',  # Disable audio to keep it minimal
                '--max-fps', '60',  # 60 FPS for smooth mirroring
                '--video-bit-rate', '8M',  # Good quality without being excessive
                '--max-size', '1920',  # Max width, maintain aspect ratio
                '--window-title', f'Phone Mirror - {device_id}'
            ]
            
            print(f"Starting scrcpy for device: {device_id}")
            print("Press Ctrl+C to stop mirroring")
            print(f"Command: {' '.join(cmd)}")
            
            # Start scrcpy process
            self.scrcpy_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait a moment to see if it starts successfully
            time.sleep(2)
            
            # Check if process is still running
            if self.scrcpy_process.poll() is not None:
                stdout, stderr = self.scrcpy_process.communicate()
                print(f"scrcpy failed to start. Exit code: {self.scrcpy_process.returncode}")
                print(f"stdout: {stdout.decode()}")
                print(f"stderr: {stderr.decode()}")
                return False
            
            print("scrcpy started successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Error starting scrcpy: {e}")
            return False
        except FileNotFoundError:
            print("Error: scrcpy not found. Please install scrcpy.")
            return False
    
    def stop_mirroring(self):
        """Stop the scrcpy mirroring process."""
        if self.scrcpy_process:
            print("Stopping mirroring...")
            self.scrcpy_process.terminate()
            try:
                self.scrcpy_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.scrcpy_process.kill()
            self.scrcpy_process = None
    
    def run(self):
        """Main execution method."""
        print("=== Minimal Phone Mirror ===")
        print("Simple Android mirroring and control via ADB")
        print()
        
        # Check prerequisites
        if not self.check_adb_installed():
            return False
        
        if not self.check_scrcpy_installed():
            return False
        
        # Get and select device
        self.device_id = self.select_device()
        if not self.device_id:
            return False
        
        # Start mirroring
        if not self.start_mirroring(self.device_id):
            return False
        
        try:
            # Keep the script running while scrcpy is active
            while self.scrcpy_process and self.scrcpy_process.poll() is None:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            self.stop_mirroring()
        
        return True


def main():
    """Main entry point."""
    mirror = PhoneMirror()
    success = mirror.run()
    
    if not success:
        print("\nMirroring failed. Please check the error messages above.")
        sys.exit(1)
    
    print("Mirroring stopped.")


if __name__ == "__main__":
    main() 