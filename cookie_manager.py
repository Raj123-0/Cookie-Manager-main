import os
import json
import base64
import sqlite3
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
import win32crypt
from Crypto.Cipher import AES

class CookieManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Local Cookie Manager (Chrome)")
        self.root.geometry("800x600")
        
        # --- File Paths ---
        self.user_data_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data")
        self.local_state_path = os.path.join(self.user_data_path, "Local State")
        self.db_path = os.path.join(self.user_data_path, "Default", "Network", "Cookies")
        self.temp_db = "Cookies_temp.db"

        self.setup_ui()
        self.encryption_key = self.get_encryption_key()

    def setup_ui(self):
        # Top Frame for Controls
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.pack(fill=tk.X)

        tk.Label(control_frame, text="Search Domain:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry = tk.Entry(control_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<Return>", lambda event: self.load_cookies())

        tk.Button(control_frame, text="Load / Refresh", command=self.load_cookies, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Delete Selected", command=self.delete_selected, bg="#f44336", fg="white").pack(side=tk.RIGHT, padx=5)

        # Middle Frame for Data Table (Treeview)
        table_frame = tk.Frame(self.root, padx=10, pady=5)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("domain", "name", "value")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("domain", text="Domain")
        self.tree.heading("name", text="Cookie Name")
        self.tree.heading("value", text="Decrypted Value")
        
        self.tree.column("domain", width=150)
        self.tree.column("name", width=150)
        self.tree.column("value", width=450)

        # Add Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bottom Frame for Status
        self.status_var = tk.StringVar()
        self.status_var.set("Ready. Click 'Load' to view cookies.")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # --- Backend Engine ---

    def get_encryption_key(self):
        try:
            with open(self.local_state_path, "r", encoding="utf-8") as f:
                local_state = json.loads(f.read())
            key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            key = key[5:] # Remove DPAPI prefix
            return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get master key.\nEnsure Chrome is installed.\n{e}")
            return None

    def decrypt_data(self, data, key):
        try:
            iv = data[3:15]
            encrypted_data = data[15:-16]
            auth_tag = data[-16:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            return cipher.decrypt_and_verify(encrypted_data, auth_tag).decode('utf-8')
        except Exception:
            return "[Decryption Failed]"

    def load_cookies(self):
        if not self.encryption_key:
            return

        # Clear existing table
        for item in self.tree.get_children():
            self.tree.delete(item)

        search_term = self.search_entry.get().strip()

        try:
            # Copy to temp file to read while Chrome is open
            shutil.copyfile(self.db_path, self.temp_db)
            conn = sqlite3.connect(self.temp_db)
            cursor = conn.cursor()

            query = "SELECT host_key, name, value, encrypted_value FROM cookies"
            if search_term:
                query += f" WHERE host_key LIKE '%{search_term}%'"

            cursor.execute(query)
            count = 0
            
            for host_key, name, value, encrypted_value in cursor.fetchall():
                decrypted_value = value if value else self.decrypt_data(encrypted_value, self.encryption_key)
                self.tree.insert("", tk.END, values=(host_key, name, decrypted_value))
                count += 1

            conn.close()
            os.remove(self.temp_db)
            self.status_var.set(f"Loaded {count} cookies.")

        except Exception as e:
            messagebox.showerror("Database Error", f"Could not read cookies.\n{e}")

    def delete_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Select", "Please select a cookie to delete.")
            return

        item_values = self.tree.item(selected_item)["values"]
        domain, name, _ = item_values

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the cookie '{name}' for '{domain}'?\n\nWARNING: Google Chrome MUST be completely closed to do this.")
        
        if confirm:
            try:
                # Target the REAL database for deletion, not the temp one
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM cookies WHERE host_key = ? AND name = ?", (domain, name))
                conn.commit()
                conn.close()

                # Remove from UI
                self.tree.delete(selected_item)
                self.status_var.set(f"Deleted cookie: {name} from {domain}")

            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    messagebox.showerror("Database Locked", "Google Chrome is currently running!\n\nYou must close Chrome completely (including background processes) before deleting or modifying cookies.")
                else:
                    messagebox.showerror("Error", f"SQLite Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CookieManagerApp(root)
    root.mainloop()
