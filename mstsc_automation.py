import time
import sys
from pywinauto import Application, Desktop
from pywinauto.keyboard import send_keys

def run_mstsc_automation():
    """
    Automates Remote Desktop Connection (MSTSC) using pywinauto:
    1. Opens Windows Search (Win+S), types MSTSC, and presses Enter.
    2. Connects to the Remote Desktop Connection window and clicks 'Connect'.
    3. Handles error dialogs: clicks 'OK', waits 20 seconds, and clicks 'Connect' again.
    """
    print("--------------------------------------------------")
    print("Starting MSTSC PyWinAuto Automation Script")
    print("--------------------------------------------------")

    # Step 1: Open Win+Search and open MSTSC
    print("\n[Step 1] Opening Windows Search and typing MSTSC...")
    send_keys('{VK_LWIN}s')
    time.sleep(1.5)
    send_keys('mstsc{ENTER}')
    time.sleep(3)

    # Step 2: Connect to Remote Desktop Connection window
    print("[Step 2] Locating Remote Desktop Connection window...")
    try:
        app = Application(backend="win32").connect(title_re=".*Remote Desktop Connection.*", timeout=10)
        dlg = app.window(title_re=".*Remote Desktop Connection.*")
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
      
