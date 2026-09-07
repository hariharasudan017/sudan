import time
import sys
from pywinauto import Application, Desktop
from pywinauto.keyboard import send_keys

def run_mstsc_automation():
    """
    Automates Remote Desktop Connection (MSTSC) using pywinauto:
    1. Launches mstsc.exe directly (bypassing Windows Search to avoid ambiguous element conflicts).
    2. Connects to the Remote Desktop Connection window and clicks 'Connect'.
    3. Handles error dialogs: clicks 'OK', waits 20 seconds, and clicks 'Connect' again.
    """
    print("--------------------------------------------------")
    print("Starting MSTSC PyWinAuto Automation Script")
    print("--------------------------------------------------")

    # Step 1 & 2: Launch MSTSC directly and target its process
    print("\n[Step 1 & 2] Launching Remote Desktop Connection...")
    try:
        try:
            # Connect to an existing MSTSC instance if already open
            app = Application(backend="win32").connect(path="mstsc.exe", timeout=2)
        except Exception:
            # Otherwise, launch mstsc.exe directly
            app = Application(backend="win32").start("mstsc.exe")

        # Target the dialog by its specific Win32 dialog class (#32770) to prevent ambiguous element matching
        dlg = app.window(class_name="#32770", title_re=".*Remote Desktop Connection.*")
        dlg.wait('ready', timeout=10)
        dlg.set_focus()

        print("Pressing 'Connect' button...")
        # Click the Connect button (Button text or control name)
        if dlg.child_window(title="&Connect", class_name="Button").exists():
            dlg.child_window(title="&Connect", class_name="Button").click()
        elif dlg.child_window(title="Connect", class_name="Button").exists():
            dlg.child_window(title="Connect", class_name="Button").click()
        else:
            # Fallback to pressing Enter key on focused dialog
            send_keys('{ENTER}')

    except Exception as e:
        print(f"Error connecting to MSTSC window: {e}")
        return

    # Step 3: Check for error popup, press OK, wait 20 seconds, press Connect again
    print("[Step 3] Checking for potential error dialogs...")
    time.sleep(3)

    try:
        desktop = Desktop(backend="win32")
        error_dlg = None

        # Look for active error dialogs with an OK button
        for win in desktop.windows():
            if win.exists() and win.is_visible():
                try:
                    if win.child_window(title="OK", class_name="Button").exists() or win.child_window(title="&OK", class_name="Button").exists():
                        # Exclude main window if it happens to have an OK button
                        if "Remote Desktop Connection" in win.window_text() and win != dlg:
                            error_dlg = win
                            break
                        elif "Error" in win.window_text() or "Warning" in win.window_text():
                            error_dlg = win
                            break
                except Exception:
                    pass

        if error_dlg:
            print("--> Error popup detected!")
            print("--> Pressing 'OK' on error dialog...")
            if error_dlg.child_window(title="OK", class_name="Button").exists():
                error_dlg.child_window(title="OK", class_name="Button").click()
            elif error_dlg.child_window(title="&OK", class_name="Button").exists():
                error_dlg.child_window(title="&OK", class_name="Button").click()
            else:
                error_dlg.set_focus()
                send_keys('{ENTER}')

            print("--> Waiting for 20 seconds...")
            time.sleep(20)

            print("--> Pressing 'Connect' again...")
            dlg.set_focus()
            if dlg.child_window(title="&Connect", class_name="Button").exists():
                dlg.child_window(title="&Connect", class_name="Button").click()
            elif dlg.child_window(title="Connect", class_name="Button").exists():
                dlg.child_window(title="Connect", class_name="Button").click()
            else:
                send_keys('{ENTER}')
            print("--> Retry 'Connect' pressed successfully.")
        else:
            print("--> No error dialog detected. Connection proceeding normally.")

    except Exception as e:
        print(f"Error during error handling check: {e}")

    print("\nAutomation completed.")

if __name__ == "__main__":
    run_mstsc_automation()
