import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import hashlib
from bank import Bank
from face_auth import FaceAuth

ADMIN_PASSWORD = "S0lx@dm1n&str4d?r\"z!"

class BankGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Banca UNI-Inicio")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        db_path = os.path.join(os.path.dirname(__file__), "db", "bank_db.json")
        self.bank = Bank(db_path)
        self.auth = FaceAuth(os.path.join(os.path.dirname(__file__), "faces"))
        self.current_dni = None
        self.is_admin = False

        self._create_widgets()

    def _create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X)
        title_label = tk.Label(
            header_frame,
            text="Bienvenid@ a Banca UNI",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)

        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Left panel: Login/Navigation
        left_panel = tk.LabelFrame(main_frame, text="Acceso", font=("Arial", 12, "bold"), bg="white", fg="#2c3e50")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10)

        tk.Label(left_panel, text="DNI (8 dígitos):", bg="white").pack(pady=5)
        self.dni_entry = tk.Entry(left_panel, width=20, font=("Arial", 11))
        self.dni_entry.pack(pady=5)

        btn_frame = tk.Frame(left_panel, bg="white")
        btn_frame.pack(pady=10)
        tk.Button(
            btn_frame,
            text="Seleccionar",
            command=self._select_account,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15
        ).pack(pady=5)

        # Logout button
        tk.Button(
            left_panel,
            text="Cerrar Sesión",
            command=self._logout,
            bg="#c0392b",
            fg="white",
            font=("Arial", 9),
            width=18
        ).pack(pady=5)

        # Admin button
        tk.Button(
            left_panel,
            text="Ingresar como Admin",
            command=self._admin_login,
            bg="#8b0000",
            fg="white",
            font=("Arial", 9, "bold"),
            width=18
        ).pack(pady=5)

        tk.Label(left_panel, text="Opciones:", font=("Arial", 11, "bold"), bg="white").pack(pady=15)

        tk.Button(
            left_panel,
            text="Crear Cuenta",
            command=self._show_create_account,
            bg="#3498db",
            fg="white",
            font=("Arial", 10),
            width=18
        ).pack(pady=5)

        tk.Button(
            left_panel,
            text="Registrar Rostro",
            command=self._enroll_face,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10),
            width=18
        ).pack(pady=5)

        # 'Listar Cuentas' movido al panel administrativo (requiere acceso Admin)

        # Right panel: Operations
        # Guardamos el LabelFrame en self para poder actualizar su texto dinámicamente
        self.right_panel = tk.LabelFrame(main_frame, text="Operaciones", font=("Arial", 12, "bold"), bg="white", fg="#2c3e50")
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        # Account info
        self.info_frame = tk.Frame(self.right_panel, bg="#ecf0f1", relief=tk.SUNKEN, bd=1)
        self.info_frame.pack(fill=tk.X, pady=10)
        self.info_label = tk.Label(
            self.info_frame,
            text="Seleccione una cuenta para comenzar",
            font=("Arial", 10),
            bg="#ecf0f1",
            justify=tk.LEFT
        )
        self.info_label.pack(padx=10, pady=10)

        # Operations buttons
        op_frame = tk.Frame(self.right_panel, bg="white")
        op_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.btn_deposit = tk.Button(
            op_frame,
            text="Depositar",
            command=self._deposit,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 11, "bold"),
            width=20,
            height=3,
            state=tk.DISABLED
        )
        self.btn_deposit.pack(pady=10)

        self.btn_withdraw = tk.Button(
            op_frame,
            text="Retirar (con verificación facial)",
            command=self._withdraw,
            bg="#e67e22",
            fg="white",
            font=("Arial", 11, "bold"),
            width=20,
            height=3,
            state=tk.DISABLED
        )
        self.btn_withdraw.pack(pady=10)

        self.btn_transfer = tk.Button(
            op_frame,
            text="Transferir (con verificación facial)",
            command=self._transfer,
            bg="#16a085",
            fg="white",
            font=("Arial", 11, "bold"),
            width=20,
            height=3,
            state=tk.DISABLED
        )
        self.btn_transfer.pack(pady=10)

        self.btn_transactions = tk.Button(
            op_frame,
            text="Ver Transacciones",
            command=self._show_transactions,
            bg="#8e44ad",
            fg="white",
            font=("Arial", 11, "bold"),
            width=20,
            height=2,
            state=tk.DISABLED
        )
        self.btn_transactions.pack(pady=10)

    def _admin_login(self):
        """Solicita contraseña de admin."""
        password = simpledialog.askstring("Acceso Admin", "Ingrese contraseña de administrador:", show="*")
        if not password:
            return
        
        if password != ADMIN_PASSWORD:
            messagebox.showerror("Error", "Contraseña incorrecta")
            return
        
        self.is_admin = True
        messagebox.showinfo("Éxito", "¡Ingresaste como admin!")
        self._show_admin_panel()

    def _show_admin_panel(self):
        """Muestra el panel administrativo."""
        admin_win = tk.Toplevel(self.root)
        admin_win.title("Panel Administrativo")
        admin_win.geometry("500x300")
        admin_win.configure(bg="white")

        # Header
        header = tk.Frame(admin_win, bg="#8b0000")
        header.pack(fill=tk.X)
        title = tk.Label(
            header,
            text="👤 Panel Administrativo",
            font=("Arial", 14, "bold"),
            bg="#8b0000",
            fg="white"
        )
        title.pack(pady=15)

        # Opciones
        content_frame = tk.Frame(admin_win, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(
            content_frame,
            text="Opciones de Administrador:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(pady=10)

        tk.Button(
            content_frame,
            text="Ver Rostros Registrados",
            command=self._admin_show_faces,
            bg="#f39c12",
            fg="white",
            font=("Arial", 11, "bold"),
            width=25,
            height=3
        ).pack(pady=10)

        tk.Button(
            content_frame,
            text="Listar Cuentas",
            command=self._admin_show_accounts,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 11, "bold"),
            width=25,
            height=2
        ).pack(pady=6)

        tk.Button(
            content_frame,
            text="Eliminar Base de Datos",
            command=self._admin_delete_database,
            bg="#c0392b",
            fg="white",
            font=("Arial", 11, "bold"),
            width=25,
            height=3
        ).pack(pady=10)

        tk.Button(
            content_frame,
            text="Cerrar Panel Admin",
            command=lambda: [admin_win.destroy(), setattr(self, 'is_admin', False)],
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10),
            width=25
        ).pack(pady=10)

    def _admin_show_faces(self):
        """Admin accede a ver rostros (requiere contraseña nuevamente)."""
        password = simpledialog.askstring("Verificación Admin", "Ingrese contraseña para confirmar:", show="*")
        if not password:
            return
        
        if password != ADMIN_PASSWORD:
            messagebox.showerror("Error", "Contraseña incorrecta")
            return
        
        self._show_faces()

    def _admin_delete_database(self):
        """Admin elimina la base de datos (requiere contraseña y confirmación)."""
        password = simpledialog.askstring("Verificación Admin", "Ingrese contraseña para confirmar:", show="*")
        if not password:
            return
        
        if password != ADMIN_PASSWORD:
            messagebox.showerror("Error", "Contraseña incorrecta")
            return
        
        # Confirmación adicional
        response = messagebox.askyesno(
            "Advertencia",
            "¿Está seguro de que desea eliminar la base de datos completamente?\n\nEsta acción no se puede deshacer."
        )
        
        if response:
            try:
                db_path = os.path.join(os.path.dirname(__file__), "db", "bank_db.json")
                if os.path.exists(db_path):
                    os.remove(db_path)
                    messagebox.showinfo("Éxito", "Base de datos eliminada correctamente")
                    # Recargar banco
                    self.bank = Bank(db_path)
                else:
                    messagebox.showinfo("Información", "No hay base de datos que eliminar")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la base de datos: {e}")

    def _admin_show_accounts(self):
        """Mostrar la lista de cuentas (admin-only, requiere contraseña)."""
        password = simpledialog.askstring("Verificación Admin", "Ingrese contraseña para confirmar:", show="*")
        if not password:
            return
        if password != ADMIN_PASSWORD:
            messagebox.showerror("Error", "Contraseña incorrecta")
            return
        self._show_accounts()

    def _select_account(self):
        dni = self.dni_entry.get().strip()
        if not dni:
            messagebox.showwarning("Advertencia", "Ingrese un DNI")
            return
        client = self.bank.get_client(dni)
        if not client:
            messagebox.showerror("Error", "Cuenta no encontrada")
            return
        
        # Solicitar PIN
        pin = simpledialog.askstring("Verificación de PIN", "Ingrese su PIN de 4 dígitos:", show="*")
        if not pin:
            messagebox.showwarning("Advertencia", "PIN cancelado")
            return
        
        if not client.verify_pin(pin):
            messagebox.showerror("Error", "PIN incorrecto")
            return
        
        self.current_dni = dni
        self._update_info()

    def _update_info(self):
        if not self.current_dni:
            self.info_label.config(text="Seleccione una cuenta para comenzar")
            # Deshabilitar botones cuando no hay sesión
            self.btn_deposit.config(state=tk.DISABLED)
            self.btn_withdraw.config(state=tk.DISABLED)
            self.btn_transfer.config(state=tk.DISABLED)
            self.btn_transactions.config(state=tk.DISABLED)
            return
        client = self.bank.get_client(self.current_dni)
        if client:
            info = f"DNI: {client.dni}\nNombre: {client.name}\nSaldo: ${client.balance:.2f}\nRostro: {'Registrado' if client.face_image else 'No registrado'}"
            self.info_label.config(text=info)
            # Habilitar botones cuando hay sesión activa
            self.btn_deposit.config(state=tk.NORMAL)
            self.btn_withdraw.config(state=tk.NORMAL)
            self.btn_transfer.config(state=tk.NORMAL)
            self.btn_transactions.config(state=tk.NORMAL)
            # Actualizar título del panel de operaciones para saludar al usuario
            try:
                self.right_panel.config(text=f"Operaciones - Bienvenid@ {client.name}")
            except Exception:
                pass

    def _show_create_account(self):
        win = tk.Toplevel(self.root)
        win.title("Crear Cuenta")
        win.geometry("400x250")
        win.configure(bg="white")

        tk.Label(win, text="Crear Nueva Cuenta", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        tk.Label(win, text="DNI (8 dígitos):", bg="white").pack(pady=5)
        dni_entry = tk.Entry(win, font=("Arial", 11), width=30)
        dni_entry.pack(pady=5)

        tk.Label(win, text="Nombre:", bg="white").pack(pady=5)
        name_entry = tk.Entry(win, font=("Arial", 11), width=30)
        name_entry.pack(pady=5)

        tk.Label(win, text="PIN (4 dígitos):", bg="white").pack(pady=5)
        pin_entry = tk.Entry(win, font=("Arial", 11), width=30, show="*")
        pin_entry.pack(pady=5)

        def create(event=None):
            dni = dni_entry.get().strip()
            name = name_entry.get().strip()
            pin = pin_entry.get().strip()
            try:
                self.bank.create_account(dni, name, pin)
                messagebox.showinfo("Éxito", f"Cuenta creada para {name}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Aceptar y Cancelar
        btn_frame = tk.Frame(win, bg="white")
        btn_frame.pack(pady=10)

        accept_btn = tk.Button(btn_frame, text="Aceptar", command=create, bg="#27ae60", fg="white", font=("Arial", 11, "bold"), width=12)
        accept_btn.pack(side=tk.LEFT, padx=5)

        def cancel():
            win.destroy()

        cancel_btn = tk.Button(btn_frame, text="Cancelar", command=cancel, bg="#95a5a6", fg="white", font=("Arial", 11), width=12)
        cancel_btn.pack(side=tk.LEFT, padx=5)

        win.bind('<Return>', create)
        dni_entry.bind('<Return>', create)
        name_entry.bind('<Return>', create)
        pin_entry.bind('<Return>', create)

    def _enroll_face(self):
        if not self.current_dni:
            messagebox.showwarning("Advertencia", "Seleccione una cuenta primero")
            return
        try:
            messagebox.showinfo("Registro de Rostro", "Se abrirá la cámara. Presione 's' para capturar, 'q' para cancelar.")
            path = self.auth.enroll_face(self.current_dni)
            self.bank.enroll_face(self.current_dni, path)
            messagebox.showinfo("Éxito", "Rostro registrado correctamente")
            self._update_info()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _deposit(self):
        if not self.current_dni:
            messagebox.showwarning("Advertencia", "Seleccione una cuenta primero")
            return
        amount_str = simpledialog.askstring("Depositar", "Monto a depositar:")
        if amount_str:
            try:
                amount = float(amount_str)
                self.bank.deposit(self.current_dni, amount)
                messagebox.showinfo("Éxito", f"Depósito de ${amount:.2f} realizado")
                self._update_info()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def _withdraw(self):
        if not self.current_dni:
            messagebox.showwarning("Advertencia", "Seleccione una cuenta primero")
            return
        amount_str = simpledialog.askstring("Retirar", "Monto a retirar:")
        if amount_str:
            try:
                amount = float(amount_str)
                messagebox.showinfo("Verificación Facial", "Se iniciará la verificación facial. Mire a la cámara.")
                ok = self.auth.verify(self.current_dni)
                if ok:
                    self.bank.withdraw(self.current_dni, amount)
                    messagebox.showinfo("Éxito", f"Retiro de ${amount:.2f} realizado")
                    self._update_info()
                else:
                    messagebox.showerror("Error", "Verificación facial fallida")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def _transfer(self):
        if not self.current_dni:
            messagebox.showwarning("Advertencia", "Seleccione una cuenta primero")
            return
        to_dni = simpledialog.askstring("Transferir", "DNI de destino:")
        if to_dni:
            amount_str = simpledialog.askstring("Transferir", "Monto a transferir:")
            if amount_str:
                try:
                    amount = float(amount_str)
                    messagebox.showinfo("Verificación Facial", "Se iniciará la verificación facial. Mire a la cámara.")
                    ok = self.auth.verify(self.current_dni)
                    if ok:
                        self.bank.transfer(self.current_dni, to_dni, amount)
                        messagebox.showinfo("Éxito", f"Transferencia de ${amount:.2f} a {to_dni} realizada")
                        self._update_info()
                    else:
                        messagebox.showerror("Error", "Verificación facial fallida")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def _show_accounts(self):
        win = tk.Toplevel(self.root)
        win.title("Cuentas Registradas")
        win.geometry("600x400")
        win.configure(bg="white")

        text_widget = tk.Text(win, font=("Courier", 10), bg="#f9f9f9")
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for c in self.bank.list_clients():
            line = f"DNI: {c.dni} | Nombre: {c.name} | Saldo: ${c.balance:.2f}\n"
            text_widget.insert(tk.END, line)

        text_widget.config(state=tk.DISABLED)

    def _show_faces(self):
        """Muestra todos los rostros registrados en una ventana."""
        faces_dir = os.path.join(os.path.dirname(__file__), "faces")
        if not os.path.exists(faces_dir):
            messagebox.showinfo("Rostros", "No hay rostros registrados aún")
            return
        
        face_files = [f for f in os.listdir(faces_dir) if f.endswith(".jpg")]
        if not face_files:
            messagebox.showinfo("Rostros", "No hay rostros registrados aún")
            return
        
        win = tk.Toplevel(self.root)
        win.title("Rostros Registrados (Admin)")
        win.geometry("700x600")
        win.configure(bg="white")
        
        # Frame para desplazamiento
        canvas = tk.Canvas(win, bg="white", highlightthickness=0)
        scroll = ttk.Scrollbar(win, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        
        for face_file in sorted(face_files):
            dni = face_file.replace(".jpg", "")
            face_path = os.path.join(faces_dir, face_file)
            
            # Frame para cada rostro
            item_frame = tk.Frame(scrollable_frame, bg="#ecf0f1", relief=tk.SUNKEN, bd=1)
            item_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Información
            info_label = tk.Label(
                item_frame,
                text=f"DNI: {dni}",
                font=("Arial", 11, "bold"),
                bg="#ecf0f1"
            )
            info_label.pack(anchor="w", padx=10, pady=5)
            
            # Ruta del archivo
            path_label = tk.Label(
                item_frame,
                text=f"Archivo: {face_file}",
                font=("Arial", 9),
                bg="#ecf0f1",
                fg="#555"
            )
            path_label.pack(anchor="w", padx=10, pady=2)
            
            # Botón para abrir imagen
            def open_image(path=face_path, dni_val=dni):
                try:
                    import subprocess
                    subprocess.Popen(["xdg-open", path])
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo abrir la imagen: {e}")
            
            tk.Button(
                item_frame,
                text="Abrir Imagen",
                command=open_image,
                bg="#3498db",
                fg="white",
                font=("Arial", 9),
                width=15
            ).pack(padx=10, pady=5)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def _show_transactions(self):
        if not self.current_dni:
            messagebox.showwarning("Advertencia", "Seleccione una cuenta primero")
            return
        client = self.bank.get_client(self.current_dni)
        if not client:
            return

        win = tk.Toplevel(self.root)
        win.title(f"Transacciones - {client.name}")
        win.geometry("600x400")
        win.configure(bg="white")

        text_widget = tk.Text(win, font=("Courier", 10), bg="#f9f9f9")
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if not client.transactions:
            text_widget.insert(tk.END, "No hay transacciones registradas")
        else:
            for i, t in enumerate(client.transactions, 1):
                line = f"{i}. {t}\n"
                text_widget.insert(tk.END, line)

        text_widget.config(state=tk.DISABLED)

    def _logout(self):
        """Cierra la sesión actual del usuario."""
        if not self.current_dni:
            messagebox.showwarning("Advertencia", "No hay sesión activa")
            return
        
        # Mostrar confirmación
        response = messagebox.askyesno(
            "Confirmar",
            f"¿Desea cerrar sesión de la cuenta {self.current_dni}?\n\nLa sesión se cerrará inmediatamente."
        )
        
        if response:
            self.current_dni = None
            self.dni_entry.delete(0, tk.END)
            self._update_info()
            messagebox.showinfo("Sesión Cerrada", "Su sesión ha sido cerrada. Por su seguridad, ingrese su DNI nuevamente.")


if __name__ == '__main__':
    root = tk.Tk()
    app = BankGUI(root)
    root.mainloop()
