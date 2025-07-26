"""Canvas coordinate utilities."""

from typing import Tuple
from ...domain.value_objects.view_type import ViewType


class CanvasCoordinateHelper:
    """Helper for coordinate transformations on a Tkinter canvas.

    * Mantiene la lógica de transformación que ya utiliza el resto de la aplicación
      (coordenadas de dominio → canvas y viceversa) pero:

        1. Usa **la misma escala en X e Y** → evita la distorsión.
        2. Centra el dibujo con un padding configurable.
        3. Invierte el eje Y solo para las vistas cuyo origen de datos es cartesiano
           (CENTER_POS_2X y LARGE_SCREEN_PIXEL_POS). Para BAMBOO_PATTERN se conserva
           el origen de imagen (0,0 en la esquina superior‑izquierda).

    Estos ajustes no afectan a los repositorios, ni al ``DataService``,
    ni a ninguna capa de dominio; solamente a la proyección sobre la interfaz.
    """

    def __init__(self, data_service, view_name: str, width: int, height: int, padding: int = 10):
        """Pre‑calcula la transformación para la vista solicitada.

        Args:
            data_service: Servicio con ``get_extents(view_name)`` y lectura de datos.
            view_name: Nombre de la vista (coincide con ``ViewType.value``).
            width:  Ancho del canvas en píxeles.
            height: Alto del canvas en píxeles.
            padding: Margen interior para no pegar el dibujo al borde.
        """
        self.data_service = data_service
        self.view_name = view_name
        self.width = width
        self.height = height

        # Extremos de los datos (min/max) recuperados del servicio existente
        self.min_x, self.min_y, self.max_x, self.max_y = data_service.get_extents(view_name)

        # Rango en cada eje (evitamos división por 0)
        range_x = self.max_x - self.min_x or 1e-9
        range_y = self.max_y - self.min_y or 1e-9

        # --- Escala uniforme: mismo factor en X e Y ---
        self.scale = min((width - 2 * padding) / range_x,
                         (height - 2 * padding) / range_y)

        # Offsets para centrar
        self.offset_x = (width  - range_x * self.scale) / 2
        self.offset_y = (height - range_y * self.scale) / 2

        # ¿Debemos invertir Y?  Solo cuando los datos están en sistema cartesiano.
        self.flip_y = (view_name != ViewType.BAMBOO_PATTERN.value)

    # --------------------------------------------------------------------- #
    #                    Conversión dominio ↔ canvas                        #
    # --------------------------------------------------------------------- #

    def to_canvas(self, x: float, y: float) -> Tuple[float, float]:
        """Convierte coordenadas de datos a coordenadas de canvas."""
        cx = (x - self.min_x) * self.scale + self.offset_x

        if self.flip_y:
            cy = self.height - ((y - self.min_y) * self.scale + self.offset_y)
        else:
            cy =            ((y - self.min_y) * self.scale + self.offset_y)
        return cx, cy

    def from_canvas(self, cx: float, cy: float) -> Tuple[float, float]:
        """Convierte coordenadas de canvas a coordenadas de datos."""
        if self.flip_y:
            y_comp = (self.height - cy - self.offset_y)
        else:
            y_comp = (cy - self.offset_y)

        x = (cx - self.offset_x) / self.scale + self.min_x
        y = y_comp / self.scale + self.min_y
        return x, y
