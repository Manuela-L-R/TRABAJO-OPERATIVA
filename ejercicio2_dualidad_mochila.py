from itertools import product


def resolver_primal_dual(weights, values, capacity):
    """Resuelve el problema de la mochila fraccionaria usando dualidad.

    Primal (continuo):
        max  sum(v_i * x_i)
        s.a. sum(w_i * x_i) <= B
             x_i >= 0

    Dual:
        min  B * y
        s.a. w_i * y >= v_i,  y >= 0

    Como sólo hay una restricción en el primal, el dual tiene una sola
    variable y, y su solución óptima se obtiene como:
        y* = max_i (v_i / w_i)
    """

    print("=== Problema primal ===")
    print("Pesos:", weights)
    print("Valores:", values)
    print("Capacidad:", capacity)
    print()

    # Cocientes valor/peso que aparecen en las restricciones duales
    ratios = [v / w for v, w in zip(values, weights)]

    print("=== Construcción del dual ===")
    print("Dual: min B * y  s.a.  w_i * y >= v_i,  y >= 0")
    for i, (w, v, r) in enumerate(zip(weights, values, ratios), start=1):
        print(f"  Artículo {i}: {w} * y >= {v}  ->  y >= {r:.4f}")
    print()

    # Método dual (caso simple con una sola variable dual)
    y_star = max(ratios)
    dual_opt = capacity * y_star

    print("=== Resolución del dual ===")
    print(f"y* = max(v_i / w_i) = {y_star:.6f}")
    print(f"Valor óptimo dual w* = B * y* = {dual_opt:.6f}")
    print()

    # Recuperar solución primal usando holgura complementaria
    eps = 1e-8
    active_indices = []
    for i, (w, v) in enumerate(zip(weights, values)):
        if abs(w * y_star - v) < eps:
            active_indices.append(i)

    print("=== Holgura complementaria y solución primal ===")
    print("Índices de restricciones duales activas (artículos):",
          [i + 1 for i in active_indices])

    x_star = [0.0] * len(weights)

    if y_star > 0:
        # En este problema la restricción de capacidad es activa:
        # sum(w_i * x_i) = B. Si sólo hay un índice activo, toda la
        # capacidad se asigna a ese artículo.
        if len(active_indices) == 1:
            j = active_indices[0]
            x_star[j] = capacity / weights[j]
        else:
            # Caso general (varios activos): aquí sólo ilustramos una
            # forma simple de obtener una solución primal factible.
            remaining = capacity
            for j in active_indices[:-1]:
                x_star[j] = 0.0
                remaining -= weights[j] * x_star[j]
            j_last = active_indices[-1]
            x_star[j_last] = remaining / weights[j_last]

    primal_opt = sum(v * x for v, x in zip(values, x_star))
    used_weight = sum(w * x for w, x in zip(weights, x_star))

    print("x* (primal) =", x_star)
    print(f"Valor óptimo primal z* = {primal_opt:.6f}")
    print(f"Peso usado = {used_weight:.6f} (de {capacity})")
    print()

    return {
        "y_star": y_star,
        "dual_opt": dual_opt,
        "x_star": x_star,
        "primal_opt": primal_opt,
        "used_weight": used_weight,
    }


def knapsack_01_bruteforce(weights, values, capacity):
    """Versión 0-1 (artículos indivisibles), para comparar.

    Explora todas las combinaciones posibles de tomar o no cada artículo
    y devuelve la mejor solución factible.
    """
    n = len(weights)
    best_val = -1.0
    best_choice = None

    for choice in product([0, 1], repeat=n):
        total_w = sum(w * x for w, x in zip(weights, choice))
        total_v = sum(v * x for v, x in zip(values, choice))
        if total_w <= capacity and total_v > best_val:
            best_val = total_v
            best_choice = choice

    return best_val, best_choice


if __name__ == "__main__":
    # Datos del ejercicio
    weights = [52, 23, 35, 15, 7]
    values = [100, 60, 70, 15, 15]
    capacity = 60

    # Resolver usando el teorema de dualidad (primal continuo y su dual)
    resultado = resolver_primal_dual(weights, values, capacity)

    # Comparar con la versión 0-1 (opcional, para interpretación práctica)
    best_val_01, best_choice_01 = knapsack_01_bruteforce(
        weights, values, capacity
    )

    print("=== Versión 0-1 (artículos indivisibles, comparación) ===")
    print("Mejor valor 0-1:", best_val_01)
    print("Elección 0-1 (1 = llevo el artículo):", best_choice_01)
