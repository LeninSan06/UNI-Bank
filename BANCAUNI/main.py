import os
import sys
import tkinter as tk
from bank import Bank
from face_auth import FaceAuth
from gui import BankGUI


DB_PATH = os.path.join(os.path.dirname(__file__), "db", "bank_db.json")


def pause():
    input("Presione Enter para continuar...")


def run_cli():
    bank = Bank(DB_PATH)
    auth = FaceAuth(os.path.join(os.path.dirname(__file__), "faces"))

    while True:
        print("\n--- Simulador Banco (reconocimiento facial) ---")
        print("1) Crear cuenta")
        print("2) Registrar rostro de cuenta")
        print("3) Depositar")
        print("4) Retirar (requiere verificación facial)")
        print("5) Transferir (requiere verificación facial)")
        print("6) Mostrar cuenta")
        print("7) Listar cuentas")
        print("0) Salir")
        opt = input("Seleccione una opción: ").strip()

        try:
            if opt == "1":
                dni = input("DNI (8 dígitos): ").strip()
                name = input("Nombre: ").strip()
                pin = input("PIN (4 dígitos): ").strip()
                bank.create_account(dni, name, pin)
                print("Cuenta creada.")
                pause()

            elif opt == "2":
                dni = input("DNI a registrar: ").strip()
                client = bank.get_client(dni)
                if not client:
                    print("Cliente no encontrado")
                else:
                    path = auth.enroll_face(dni)
                    bank.enroll_face(dni, path)
                pause()

            elif opt == "3":
                dni = input("DNI: ").strip()
                amount = float(input("Monto a depositar: "))
                bank.deposit(dni, amount)
                print("Depósito realizado.")
                pause()

            elif opt == "4":
                dni = input("DNI: ").strip()
                amount = float(input("Monto a retirar: "))
                # verificación facial
                try:
                    ok = auth.verify(dni)
                except Exception as e:
                    print("Error durante verificación:", e)
                    ok = False
                if ok:
                    bank.withdraw(dni, amount)
                    print("Retiro exitoso.")
                else:
                    print("No se pudo verificar identidad. Retiro cancelado.")
                pause()

            elif opt == "5":
                from_dni = input("DNI origen: ").strip()
                to_dni = input("DNI destino: ").strip()
                amount = float(input("Monto a transferir: "))
                try:
                    ok = auth.verify(from_dni)
                except Exception as e:
                    print("Error durante verificación:", e)
                    ok = False
                if ok:
                    bank.transfer(from_dni, to_dni, amount)
                    print("Transferencia completada.")
                else:
                    print("No se pudo verificar identidad. Transferencia cancelada.")
                pause()

            elif opt == "6":
                dni = input("DNI: ").strip()
                c = bank.get_client(dni)
                if not c:
                    print("Cliente no encontrado")
                else:
                    print(f"DNI: {c.dni}")
                    print(f"Nombre: {c.name}")
                    print(f"Saldo: {c.balance}")
                    print(f"Imagen: {c.face_image}")
                    print("Transacciones:")
                    for t in c.transactions:
                        print("-", t)
                pause()

            elif opt == "7":
                for c in bank.list_clients():
                    print(f"{c.dni} - {c.name} - {c.balance}")
                pause()

            elif opt == "0":
                print("Saliendo...")
                break

            else:
                print("Opción no válida")
        except Exception as e:
            print("Error:", e)
            pause()


def run_gui():
    root = tk.Tk()
    app = BankGUI(root)
    root.mainloop()


def main():
    print("\n=== Simulador de Banco ===")
    print("1) Interfaz Gráfica (GUI)")
    print("2) Terminal (CLI)")
    choice = input("Seleccione interfaz (1 o 2): ").strip()

    if choice == "1":
        print("Iniciando interfaz gráfica...")
        run_gui()
    elif choice == "2":
        print("Iniciando terminal...")
        run_cli()
    else:
        print("Opción no válida. Usando GUI por defecto.")
        run_gui()


if __name__ == '__main__':
    main()
