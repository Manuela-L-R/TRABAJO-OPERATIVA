"""
PROBLEMA DEL EXCURSIONISTA - MOCHILA 0/1 (KNAPSACK)
Maximizar valor de artículos sin exceder el peso límite de 60 libras
"""

from pulp import *
import pandas as pd

# ==================== DATA DEL PROBLEMA ====================
articulos = ['Artículo 1', 'Artículo 2', 'Artículo 3', 'Artículo 4', 'Artículo 5']
pesos = [52, 23, 35, 15, 7]  # en libras
valores = [100, 60, 70, 15, 15]
peso_maximo = 60

print("=" * 80)
print("PROBLEMA DEL EXCURSIONISTA - MOCHILA 0/1 (KNAPSACK)")
print("=" * 80)

print("\n📦 DATA DEL PROBLEMA:")
data_df = pd.DataFrame({
    'Artículo': articulos,
    'Peso (libras)': pesos,
    'Valor': valores
})
print(data_df.to_string(index=False))
print(f"\n🎒 Peso máximo que puede cargar: {peso_maximo} libras")

# ==================== MODELO PRIMAL ====================
print("\n" + "=" * 80)
print("MODELO: MAXIMIZAR VALOR DE MOCHILA")
print("=" * 80)

prob = LpProblem("Mochila_Excursionista", LpMaximize)

# Variables de decisión: binarias (0 = no llevar, 1 = llevar)
x = [LpVariable(f"x_{i+1}", cat='Binary') for i in range(5)]

# Función objetivo: Maximizar valor total
prob += lpSum([valores[i] * x[i] for i in range(5)]), "Valor_Total"

# Restricción: No exceder peso máximo
prob += lpSum([pesos[i] * x[i] for i in range(5)]) <= peso_maximo, "Restriccion_Peso"

print("\nFORMULACIÓN MATEMÁTICA:")
print("\nVariables de decisión:")
print("x_i = 1 si se lleva el artículo i, 0 si no se lleva (i=1,2,3,4,5)")

print("\nFunción Objetivo (Maximizar):")
print("Z = 100*x_1 + 60*x_2 + 70*x_3 + 15*x_4 + 15*x_5")

print("\nRestricciones:")
print(f"52*x_1 + 23*x_2 + 35*x_3 + 15*x_4 + 7*x_5 ≤ {peso_maximo}")
print("x_i ∈ {0, 1}, para todo i = 1,2,3,4,5 (binarias)")

# ==================== RESOLVER ====================
print("\n" + "-" * 80)
print("RESOLUCIÓN")
print("-" * 80)

prob.solve(PULP_CBC_CMD(msg=0))

print(f"\nEstatus: {LpStatus[prob.status]}")
print(f"\n✓ VALOR MÁXIMO OBTENIDO: {int(value(prob.objective))}")

# ==================== SOLUCIÓN ====================
print("\n" + "=" * 80)
print("SOLUCIÓN ÓPTIMA")
print("=" * 80)

solucion = []
peso_total = 0
valor_total = 0

print("\n🎒 Artículos a llevar:")
print("-" * 80)

for i in range(5):
    if value(x[i]) == 1:
        solucion.append(i)
        peso_total += pesos[i]
        valor_total += valores[i]
        print(f"✓ {articulos[i]:12} - Peso: {pesos[i]:2} libras | Valor: {valores[i]:3}")

print("-" * 80)
print(f"TOTALES:")
print(f"  Peso total:  {peso_total} / {peso_maximo} libras")
print(f"  Valor total: {valor_total} unidades")
print(f"  Peso disponible: {peso_maximo - peso_total} libras")

# ==================== ANÁLISIS DETALLADO ====================
print("\n" + "=" * 80)
print("ANÁLISIS DETALLADO DE LA SOLUCIÓN")
print("=" * 80)

tabla_solucion = []
for i in range(5):
    tabla_solucion.append({
        'Artículo': articulos[i],
        'Peso': pesos[i],
        'Valor': valores[i],
        'Relación V/P': f"{valores[i]/pesos[i]:.3f}",
        'Seleccionar': '✓ SÍ' if value(x[i]) == 1 else '✗ NO'
    })

solucion_df = pd.DataFrame(tabla_solucion)
print("\n" + solucion_df.to_string(index=False))

print("\n💡 OBSERVACIONES:")
print(f"  • Se seleccionan {len(solucion)} artículos")
print(f"  • Peso utilizado: {peso_total}/{peso_maximo} libras ({peso_total*100//peso_maximo}%)")
print(f"  • Espacio disponible: {peso_maximo - peso_total} libras")
print(f"  • Valor obtenido: {valor_total} unidades")
print(f"  • Ratio valor/peso promedio: {valor_total/peso_total:.3f}")

# ==================== ANÁLISIS ALTERNATIVO ====================
print("\n" + "=" * 80)
print("ANÁLISIS ALTERNATIVO (POR RATIO VALOR/PESO)")
print("=" * 80)

ratios = [(i, valores[i]/pesos[i]) for i in range(5)]
ratios_ordenados = sorted(ratios, key=lambda x: x[1], reverse=True)

print("\nArticulos ordenados por ratio Valor/Peso (Mayor a Menor):")
print("-" * 80)

peso_acum = 0
valor_acum = 0
seleccionados_alt = []

for idx, (i, ratio) in enumerate(ratios_ordenados):
    print(f"{idx+1}. {articulos[i]:12} | Peso: {pesos[i]:2} | Valor: {valores[i]:3} | Ratio: {ratio:.3f}", end="")
    
    if peso_acum + pesos[i] <= peso_maximo:
        peso_acum += pesos[i]
        valor_acum += valores[i]
        seleccionados_alt.append(i)
        print(" ✓ TOMAR")
    else:
        print(" ✗ No cabe")

print("-" * 80)
print(f"\nMétodo heurístico (greed): Valor = {valor_acum} (menor que óptimo)")
print(f"Método óptimo: Valor = {valor_total} (mejor)")

# ==================== CONCLUSIÓN ====================
print("\n" + "=" * 80)
print("RESUMEN Y RECOMENDACIÓN")
print("=" * 80)

print(f"""
✓ RESPUESTA:
  El excursionista debe llevar los siguientes artículos para maximizar valor:
  
  Artículos seleccionados:
""")

for i in solucion:
    print(f"    • {articulos[i]:12} (Peso: {pesos[i]} lb, Valor: {valores[i]})")

print(f"""
  Peso total: {peso_total} libras (máximo permitido: {peso_maximo})
  Valor total: {valor_total} unidades
  
✓ BENEFICIO:
  Lleva los artículos más valiosos respecto a su peso
  Bajo este criterio, obtiene el máximo valor posible
  
✓ EFICIENCIA:
  Utiliza {peso_maximo - peso_total} libras adicionales de capacidad
  (No hay artículos restantes que quepan)
""")

# ==================== EXPORTAR RESULTADOS ====================
resultados = {
    'articulos_seleccionados': [articulos[i] for i in solucion],
    'peso_total': peso_total,
    'valor_total': valor_total,
    'indice_seleccion': solucion
}

print("\n" + "=" * 80)
print("DATOS PARA LA PÁGINA WEB")
print("=" * 80)
print(f"\nArticulos a llevar: {', '.join([str(i+1) for i in solucion])}")
print(f"Peso total: {peso_total}")
print(f"Valor total: {valor_total}")
