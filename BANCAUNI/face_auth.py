import os
import cv2
import time
from typing import Optional


class FaceAuth:
    """Autenticación sencilla con OpenCV usando ORB feature matching.

    - `enroll_face(dni)`: captura una imagen de referencia y la guarda en `faces_dir`.
    - `verify(dni, timeout)`: compara la imagen en vivo con la referencia usando ORB.
    """

    def __init__(self, faces_dir: str = None):
        self.faces_dir = faces_dir or os.path.join(os.path.dirname(__file__), "faces")
        os.makedirs(self.faces_dir, exist_ok=True)

    def _face_path(self, dni: str) -> str:
        return os.path.join(self.faces_dir, f"{dni}.jpg")

    def enroll_face(self, dni: str, camera_index: int = 0) -> str:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            cap.release()
            raise RuntimeError("No se puede abrir la cámara")
        print("Presione 's' para capturar la foto de referencia. Presione 'q' para cancelar.")
        saved_path = self._face_path(dni)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Enroll - Presione s para guardar", frame)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('s'):
                cv2.imwrite(saved_path, frame)
                print(f"Imagen guardada en: {saved_path}")
                break
            if k == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        return saved_path

    def verify(self, dni: str, camera_index: int = 0, timeout: int = 10, threshold: float = 0.12) -> bool:
        """Verifica que la cara capturada coincida con la imagen de referencia.

        threshold: valor empírico de ratio de matches buenas (0..1). Ajustar según necesidad.
        """
        ref_path = self._face_path(dni)
        if not os.path.exists(ref_path):
            raise FileNotFoundError("No existe imagen de referencia para este DNI. Por favor registre la cara primero.")

        ref_img = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
        if ref_img is None:
            raise RuntimeError("No se pudo leer la imagen de referencia")

        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            cap.release()
            raise RuntimeError("No se puede abrir la cámara")

        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(ref_img, None)

        start = time.time()
        print("Iniciando verificación facial: mire a la cámara...")
        result = False
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            kp2, des2 = orb.detectAndCompute(gray, None)
            if des1 is None or des2 is None or len(kp1) < 5 or len(kp2) < 5:
                # not enough features yet
                cv2.imshow("Verificación", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                if time.time() - start > timeout:
                    break
                continue

            
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
            matches = bf.knnMatch(des1, des2, k=2)
            
            good = []
            for m_n in matches:
                if len(m_n) != 2:
                    continue
                m, n = m_n
                if m.distance < 0.75 * n.distance:
                    good.append(m)

            
            denom = min(len(kp1), len(kp2))
            ratio = (len(good) / denom) if denom > 0 else 0.0
            cv2.putText(frame, f"Match ratio: {ratio:.3f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.imshow("Verificación", frame)

            if ratio >= threshold:
                result = True
                print("Verificación facial exitosa")
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if time.time() - start > timeout:
                break

        cap.release()
        cv2.destroyAllWindows()
        if not result:
            print("Verificación facial fallida")
        return result
