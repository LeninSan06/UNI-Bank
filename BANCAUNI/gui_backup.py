import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
from bank import Bank
from face_auth import FaceAuth


class BankGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Banco - Reconocimiento Facial")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        db_path = os.path.join(os.path.dirname(__file__), "db", "bank_db.json")
        self.bank = Bank(db_path)
        self.auth = FaceAuth(os.path.join(os.path.dirname(__file__), "faces"))
        self.current_dni = None

        self._create_widgets()

    def _create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X)
        title_label = tk.Label(
            header_frame,
            text="🏦 Bienvenid@ a Banca UNI",
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

        tk.Button(
            left_panel,
            text="Listar Cuentas",
            command=self._show_accounts,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 10),
            width=18
        ).pack(pady=5)

        # Right panel: Operations
        right_panel = tk.LabelFrame(main_frame, text="Operaciones", font=("Arial", 12, "bold"), bg="white", fg="#2c3e50")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        # Account info
        self.info_frame = tk.Frame(right_panel, bg="#ecf0f1", relief=tk.SUNKEN, bd=1)
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
        op_frame = tk.Frame(right_panel, bg="white")
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

        #Aceptar y Cancelar
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
