import json
import os
from typing import Dict, List, Optional


class Client:
    def __init__(self, dni: str, name: str, balance: float = 0.0, face_image: Optional[str] = None, pin: Optional[str] = None):
        self.dni = dni
        self.name = name
        self.balance = float(balance)
        self.face_image = face_image
        self.pin = pin  # PIN de 4 dígitos
        self.transactions: List[Dict] = []

    def to_dict(self):
        return {
            "dni": self.dni,
            "name": self.name,
            "balance": self.balance,
            "face_image": self.face_image,
            "pin": self.pin,
            "transactions": self.transactions,
        }

    @staticmethod
    def from_dict(d):
        c = Client(d["dni"], d["name"], d.get("balance", 0.0), d.get("face_image"), d.get("pin"))
        c.transactions = d.get("transactions", [])
        return c

    def verify_pin(self, pin: str) -> bool:
        """Verifica si el PIN es correcto."""
        return self.pin == pin


class Bank:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.clients: Dict[str, Client] = {}
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._load()

    def _load(self):
        if not os.path.exists(self.db_path):
            self._save()
        with open(self.db_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception:
                data = {}
        self.clients = {dni: Client.from_dict(v) for dni, v in data.items()}

    def _save(self):
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump({dni: c.to_dict() for dni, c in self.clients.items()}, f, indent=2, ensure_ascii=False)

    def validate_dni(self, dni: str) -> bool:
        return dni.isdigit() and len(dni) == 8

    def create_account(self, dni: str, name: str, pin: str) -> bool:
        if not self.validate_dni(dni):
            raise ValueError("DNI inválido: debe tener 8 dígitos")
        if not pin or not pin.isdigit() or len(pin) != 4:
            raise ValueError("PIN debe ser 4 dígitos numéricos")
        if dni in self.clients:
            raise ValueError("Cuenta ya existe")
        self.clients[dni] = Client(dni, name, pin=pin)
        self._save()
        return True

    def enroll_face(self, dni: str, face_image_path: str):
        client = self.clients.get(dni)
        if not client:
            raise KeyError("Cliente no encontrado")
        client.face_image = face_image_path
        client.transactions.append({"type": "enroll_face", "path": face_image_path})
        self._save()

    def deposit(self, dni: str, amount: float):
        if amount <= 0:
            raise ValueError("Monto debe ser positivo")
        client = self.clients.get(dni)
        if not client:
            raise KeyError("Cliente no encontrado")
        client.balance += float(amount)
        client.transactions.append({"type": "deposit", "amount": amount})
        self._save()

    def withdraw(self, dni: str, amount: float):
        if amount <= 0:
            raise ValueError("Monto debe ser positivo")
        client = self.clients.get(dni)
        if not client:
            raise KeyError("Cliente no encontrado")
        if client.balance < amount:
            raise ValueError("Fondos insuficientes")
        client.balance -= float(amount)
        client.transactions.append({"type": "withdraw", "amount": amount})
        self._save()

    def transfer(self, from_dni: str, to_dni: str, amount: float):
        if amount <= 0:
            raise ValueError("Monto debe ser positivo")
        src = self.clients.get(from_dni)
        dst = self.clients.get(to_dni)
        if not src or not dst:
            raise KeyError("Cliente origen o destino no encontrado")
        if src.balance < amount:
            raise ValueError("Fondos insuficientes")
        src.balance -= float(amount)
        dst.balance += float(amount)
        src.transactions.append({"type": "transfer_out", "amount": amount, "to": to_dni})
        dst.transactions.append({"type": "transfer_in", "amount": amount, "from": from_dni})
        self._save()

    def get_client(self, dni: str) -> Optional[Client]:
        return self.clients.get(dni)

    def list_clients(self):
        return list(self.clients.values())
