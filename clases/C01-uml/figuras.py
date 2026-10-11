"""Figuras del apunte de C01 con la estética de la cátedra. Se ejecuta desde scripts/docx/build.py."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts", "docx"))
from catedra import *  # noqa: E402,F401,F403

OUT = os.path.join(os.path.dirname(__file__), "figuras")
os.makedirs(OUT, exist_ok=True)


def fig_anatomia():
    s = Svg(560, 200)
    x, y, w = 110, 20, 360
    s.class_box("p", x, y, w, "Pedido",
                ["- fecha: Fecha", "- estado: Estado", "- cliente: Cliente"],
                ["+ calcularTotal(): Decimal", "+ confirmar(): void"])
    bx, by, bw, bh = s.boxes["p"]
    for n, cy in ((1, by + 17), (2, by + 34 + 36), (3, by + 34 + 72 + 26)):
        s.line([(x - 44 + 11, cy), (x, cy)], color="#1f4e79", width=1.4)
        callout(s, x - 44, cy, n)
    return s


def fig_clases():
    s = Svg(760, 390)
    s.class_box("cli", 10, 30, 150, "Cliente", ["- nombre: String", "- email: String"])
    s.class_box("ped", 290, 30, 200, "Pedido", ["- fecha: Fecha", "- estado: Estado"], ["+ calcularTotal(): Decimal"])
    s.class_box("mp", 570, 30, 185, "MedioDePago", [], ["+ pagar(monto): Boolean"], stereotype="interface")
    s.class_box("pro", 10, 250, 150, "Producto", ["- nombre: String", "- precio: Decimal"])
    s.class_box("lin", 290, 250, 200, "LíneaDePedido", ["- cantidad: Entero"], ["+ subtotal(): Decimal"])
    s.class_box("tar", 545, 250, 120, "Tarjeta", ["- titular: String"])
    s.class_box("efe", 680, 250, 75, "Efectivo")
    # asociación Cliente - Pedido
    s.line([(160, 75), (290, 75)], color=BORDE, width=2)
    s.text(168, 68, "1", size=14, bold=True)
    s.text(272, 68, "*", size=16, bold=True, anchor="end")
    s.text(225, 96, "realiza", italic=True, anchor="middle")
    # Pedido -> MedioDePago (navegable)
    s.line([(490, 60), (570, 60)], color=BORDE, width=2, end="abierta")
    s.text(530, 52, "1", size=14, bold=True, anchor="middle")
    s.text(530, 82, "paga con", italic=True, anchor="middle")
    # composición Pedido <>-- LíneaDePedido
    s.line([(390, 148), (390, 250)], color=BORDE, width=2, start="rombo")
    s.text(398, 242, "*", size=16, bold=True)
    # LíneaDePedido -> Producto (navegable)
    s.line([(290, 300), (160, 300)], color=BORDE, width=2, end="abierta")
    s.text(278, 292, "*", size=16, bold=True, anchor="end")
    s.text(172, 292, "1", size=14, bold=True)
    # realizaciones
    for cx in (605, 717):
        s.line([(cx, 250), (cx, 124)], color=BORDE, width=2, dashed=True, end="tri")
    return s


def fig_objetos():
    s = Svg(760, 400)
    s.class_box("ana", 10, 20, 165, "ana: Cliente", ['nombre = "Ana"'], obj=True)
    s.class_box("p1", 285, 20, 190, "pedido1: Pedido", ["fecha = 12/03", "estado = PENDIENTE"], obj=True)
    s.class_box("t1", 585, 20, 165, "t1: Tarjeta", ['titular = "Ana"'], obj=True)
    s.class_box("l1", 155, 170, 190, "l1: LíneaDePedido", ["cantidad = 2"], obj=True)
    s.class_box("l2", 475, 170, 190, "l2: LíneaDePedido", ["cantidad = 1"], obj=True)
    s.class_box("a", 155, 290, 190, "p1: Producto", ['nombre = "Teclado"', "precio = 18000"], obj=True)
    s.class_box("b", 475, 290, 190, "p2: Producto", ['nombre = "Mouse"', "precio = 9500"], obj=True)
    s.line([(175, 53), (285, 53)], color=BORDE, width=2)
    s.text(230, 45, "realiza", italic=True, anchor="middle")
    s.line([(475, 53), (585, 53)], color=BORDE, width=2)
    s.text(530, 45, "paga con", italic=True, anchor="middle")
    s.line([(330, 106), (330, 138), (250, 138), (250, 170)], color=BORDE, width=2)
    s.line([(430, 106), (430, 138), (570, 138), (570, 170)], color=BORDE, width=2)
    s.line([(250, 236), (250, 290)], color=BORDE, width=2)
    s.line([(570, 236), (570, 290)], color=BORDE, width=2)
    return s


def fig_secuencia():
    s = Svg(760, 500)
    marco_sd(s, "ConfirmarPedido")
    X_CLI, X_PED, X_LIN, X_MP = 100, 290, 490, 670
    actor(s, X_CLI, 52, "Cliente")
    cabecera(s, X_PED, 62, ":Pedido", 100)
    cabecera(s, X_LIN, 62, ":LíneaDePedido", 150)
    cabecera(s, X_MP, 62, ":MedioDePago", 135)
    for x, y0 in ((X_CLI, 140), (X_PED, 94), (X_LIN, 94), (X_MP, 94)):
        linea_vida(s, x, y0, 470)
    activacion(s, X_PED, 160, 440)
    activacion(s, X_LIN, 250, 310)
    activacion(s, X_MP, 380, 430)
    fragmento(s, 104, 196, 496, 140, "loop", "[por cada línea]")
    mensaje(s, X_CLI, X_PED - 6, 160, "confirmar()")
    mensaje(s, X_PED + 6, X_LIN - 6, 250, "subtotal()")
    mensaje(s, X_LIN - 6, X_PED + 6, 304, "monto", "return")
    mensaje(s, X_PED + 6, X_MP - 6, 380, "pagar(total)")
    mensaje(s, X_MP - 6, X_PED + 6, 426, "true", "return")
    return s


if __name__ == "__main__":
    for nombre, fn in (("anatomia", fig_anatomia), ("clases", fig_clases), ("objetos", fig_objetos), ("secuencia", fig_secuencia)):
        fn().save(os.path.join(OUT, nombre + ".svg"))
        print(nombre)
