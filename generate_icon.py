"""
Script para generar el icono oficial de la aplicación en formatos .ico y .png.
Representa la descomposición matricial LU con una estética moderna y limpia.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


def create_app_icon():
    size = (256, 256)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Fondo cuadrado con esquinas redondeadas
    bg_color = (15, 23, 42, 255)       # Slate 900
    border_color = (37, 99, 235, 255)   # Azul 600
    draw.rounded_rectangle([8, 8, 247, 247], radius=48, fill=bg_color, outline=border_color, width=4)

    # 2. Triángulo superior U (sombreado sutil azul/índigo)
    u_triangle = [(36, 36), (220, 36), (220, 220)]
    draw.polygon(u_triangle, fill=(30, 58, 138, 160))   # Azul oscuro traslúcido

    # 3. Triángulo inferior L (sombreado sutil cian/azul)
    l_triangle = [(36, 36), (36, 220), (220, 220)]
    draw.polygon(l_triangle, fill=(15, 118, 110, 140))  # Verde azulado traslúcido

    # 4. Línea diagonal de la matriz (separador L y U)
    draw.line([(34, 34), (222, 222)], fill=(56, 189, 248, 255), width=6)  # Celeste brillante

    # 5. Letras L y U tipográficas
    # Intentamos cargar una fuente limpia del sistema o dibujamos geometrías nítidas
    try:
        font_large = ImageFont.truetype("arialbd.ttf", 68)
    except Exception:
        font_large = ImageFont.load_default()

    # Letra L en la región inferior
    draw.text((70, 125), "L", fill=(255, 255, 255, 255), font=font_large)

    # Letra U en la región superior
    draw.text((145, 55), "U", fill=(125, 211, 252, 255), font=font_large)

    # 6. Pequeños puntos de matriz en las esquinas opuestas para dar identidad matricial
    dot_color = (148, 163, 184, 180)
    for x, y in [(60, 60), (196, 196)]:
        draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=dot_color)

    # Guardar en PNG de alta resolución
    img.save("icon.png", format="PNG")

    # Guardar en ICO con múltiples resoluciones (para Windows y PyCharm)
    icon_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save("icon.ico", format="ICO", sizes=icon_sizes)

    print("Iconos 'icon.png' e 'icon.ico' generados exitosamente.")


if __name__ == "__main__":
    create_app_icon()
