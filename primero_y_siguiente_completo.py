# =============================================================================
#  Calculadora de conjuntos PRIMERO y SIGUIENTE
#  Diseño de Lenguajes de Programación
#
#  – compute_first, get_first, get_terminals, gramáticas de prueba
#  – compute_follow, parse_grammar, print_results, menú interactivo
#  
#  Integrantes: Alejandro Antón 221041 y Ruth de León 22428
#
#  Link de Github: https://github.com/Anton17303/Laboratorio_3_DDA.git
# =============================================================================

EPSILON = 'ε'
DOLLAR  = '$'


# =============================================================================
#   GRAMÁTICAS DE PRUEBA (formato dict, para ejecución rápida)
# =============================================================================

GRAMMAR_DICT_1 = {
    "E" : ["T E'"],
    "E'": ["+ T E'", "ε"],
    "T" : ["F T'"],
    "T'": ["* F T'", "ε"],
    "F" : ["( E )", "id"]
}

GRAMMAR_DICT_2 = {
    "S": ["A B"],
    "A": ["a A", "ε"],
    "B": ["b B", "c"]
}


# =============================================================================
#   PARSING — convierte texto libre a estructura interna
# =============================================================================

def is_non_terminal(sym: str) -> bool:
    """
    Retorna True si el símbolo es un no terminal.
    Convención: empieza con letra mayúscula (soporta E', T', S1, etc.).
    """
    return bool(sym) and sym[0].isupper()


def parse_grammar(text: str):
    """
    Parsea texto con producciones en formato:
        E  -> T E'
        E' -> + T E' | ε

    Acepta  'ε', 'eps'  o  'epsilon'  como símbolo vacío.

    Retorna
    -------
    productions   : dict[str, list[list[str]]]   NT → lista de alternativas
    start_symbol  : str                           primer NT declarado
    non_terminals : set[str]
    terminals     : set[str]
    """
    productions: dict[str, list[list[str]]] = {}
    start_symbol = None

    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        if '->' not in line:
            raise ValueError(f'Línea inválida (falta "->"): "{line}"')

        lhs, rhs = line.split('->', 1)
        lhs = lhs.strip()

        if not is_non_terminal(lhs):
            raise ValueError(f'Símbolo izquierdo inválido: "{lhs}"')

        if start_symbol is None:
            start_symbol = lhs
        if lhs not in productions:
            productions[lhs] = []

        for alt in rhs.split('|'):
            alt = alt.strip()
            if alt in ('ε', 'eps', 'epsilon', ''):
                productions[lhs].append([EPSILON])
            else:
                tokens = alt.split()
                tokens = [EPSILON if t in ('eps', 'epsilon', 'ε') else t
                          for t in tokens]
                productions[lhs].append(tokens)

    if not start_symbol:
        raise ValueError('La gramática está vacía.')

    non_terminals = set(productions.keys())
    terminals: set[str] = set()
    for rules in productions.values():
        for rule in rules:
            for sym in rule:
                if sym != EPSILON and sym not in non_terminals:
                    terminals.add(sym)

    return productions, start_symbol, non_terminals, terminals


def dict_to_productions(grammar_dict: dict):
    """
    Convierte una gramática en formato dict 
    al formato interno list[list[str]] que usa el resto del programa.

    El símbolo inicial es la primera clave del diccionario.
    """
    productions: dict[str, list[list[str]]] = {}
    start_symbol = None

    for lhs, alts in grammar_dict.items():
        if start_symbol is None:
            start_symbol = lhs
        productions[lhs] = []
        for alt in alts:
            tokens = alt.split()
            tokens = [EPSILON if t in ('eps', 'epsilon', 'ε') else t
                      for t in tokens]
            productions[lhs].append(tokens if tokens else [EPSILON])

    non_terminals = set(productions.keys())
    terminals: set[str] = set()
    for rules in productions.values():
        for rule in rules:
            for sym in rule:
                if sym != EPSILON and sym not in non_terminals:
                    terminals.add(sym)

    return productions, start_symbol, non_terminals, terminals


# =============================================================================
#  TERMINALES — extracción desde gramática dict
# =============================================================================

def get_terminals(grammar: dict) -> set:
    """
    Obtiene el conjunto de terminales de una gramática en formato dict.
    Un terminal es cualquier símbolo que no sea NT ni ε.
    """
    non_terminals = set(grammar.keys())
    terminals = set()

    for productions in grammar.values():
        for prod in productions:
            for symbol in prod.split():
                if symbol not in non_terminals and symbol != EPSILON:
                    terminals.add(symbol)

    return terminals


# =============================================================================
#   FIRST — cálculo de conjuntos PRIMERO
# =============================================================================

def first_of_string(symbols: list,
                    first:   dict,
                    non_terminals: set) -> set:
    """
    Calcula FIRST de una cadena de símbolos  α = X₁ X₂ … Xₙ.

    Algoritmo:
      · Agregar FIRST(X₁) − {ε}.
      · Si ε ∈ FIRST(X₁) → continuar con X₂, y así sucesivamente.
      · Si todos los Xᵢ derivan ε → agregar ε al resultado.
    """
    result: set[str] = set()

    if not symbols:
        result.add(EPSILON)
        return result

    for sym in symbols:
        if sym == EPSILON:
            result.add(EPSILON)
            break
        elif sym in non_terminals:
            result |= first[sym] - {EPSILON}
            if EPSILON not in first[sym]:
                break       # este símbolo no es anulable; nos detenemos
        else:
            result.add(sym) # terminal ordinario
            break
    else:
        # todos los símbolos de la cadena pueden derivar ε
        result.add(EPSILON)

    return result


def compute_first(productions:   dict,
                  non_terminals: set) -> dict[str, set]:
    """
    Calcula FIRST(A) para cada no terminal A por punto fijo.

    Reglas:
      1. A → ε                    ⇒  ε ∈ FIRST(A)
      2. A → a α  (a terminal)    ⇒  a ∈ FIRST(A)
      3. A → B α  (B no terminal) ⇒  FIRST(B)−{ε} ⊆ FIRST(A)
                                      Si ε ∈ FIRST(B) → aplicar sobre α
    """
    first: dict[str, set] = {nt: set() for nt in non_terminals}

    changed = True
    while changed:
        changed = False
        for lhs, rules in productions.items():
            for rule in rules:
                f = first_of_string(rule, first, non_terminals)
                before = len(first[lhs])
                first[lhs] |= f
                if len(first[lhs]) > before:
                    changed = True

    return first


def get_first(grammar_dict: dict) -> dict[str, set]:
    """
    Interfaz de alto nivel :
    recibe gramática en formato dict y devuelve FIRST.
    """
    productions, _, non_terminals, _ = dict_to_productions(grammar_dict)
    return compute_first(productions, non_terminals)


# =============================================================================
#   FOLLOW — cálculo de conjuntos SIGUIENTE
# =============================================================================

def compute_follow(productions:   dict,
                   non_terminals: set,
                   start_symbol:  str,
                   first:         dict[str, set]) -> dict[str, set]:
    """
    Calcula FOLLOW(A) para cada no terminal A por punto fijo.

    Reglas:
      1. FOLLOW(start) contiene $
      2. A → α B β  ⇒  FOLLOW(B) ⊇ FIRST(β) − {ε}
      3. A → α B β  y ε ∈ FIRST(β)  ⇒  FOLLOW(B) ⊇ FOLLOW(A)
         (aplica también cuando β es vacío)
    """
    follow: dict[str, set] = {nt: set() for nt in non_terminals}
    follow[start_symbol].add(DOLLAR)    # Regla 1

    changed = True
    while changed:
        changed = False
        for lhs, rules in productions.items():
            for rule in rules:
                for i, B in enumerate(rule):
                    if B not in non_terminals:
                        continue        # sólo no terminales

                    beta = rule[i + 1:]

                    # Regla 2
                    first_beta = first_of_string(beta, first, non_terminals)
                    to_add = first_beta - {EPSILON}
                    before = len(follow[B])
                    follow[B] |= to_add
                    if len(follow[B]) > before:
                        changed = True

                    # Regla 3: β ⇒* ε  (o β vacío)
                    if not beta or EPSILON in first_beta:
                        before = len(follow[B])
                        follow[B] |= follow[lhs]
                        if len(follow[B]) > before:
                            changed = True

    return follow


# =============================================================================
#   SALIDA — formateo e impresión de resultados
# =============================================================================

def fmt_set(s: set[str]) -> str:
    """Formatea un conjunto: $ primero, ε al final, resto en orden alfabético."""
    ordered = []
    if DOLLAR  in s: ordered.append(DOLLAR)
    ordered += sorted(x for x in s if x not in (DOLLAR, EPSILON))
    if EPSILON in s: ordered.append(EPSILON)
    return '{ ' + ', '.join(ordered) + ' }'


def print_separator(char: str = '─', width: int = 60):
    print(char * width)


def print_results(productions, start_symbol, non_terminals, terminals,
                  first, follow):
    """Imprime resultados de forma clara y estructurada (req. 5 del laboratorio)."""
    print_separator('═')
    print('  RESULTADOS')
    print_separator('═')

    nts_sorted = [start_symbol] + sorted(non_terminals - {start_symbol})
    ts_sorted  = sorted(terminals)

    # Req. 2 — Símbolos terminales y no terminales
    print(f'\n  No terminales : {", ".join(nts_sorted)}')
    print(f'  Terminales    : {", ".join(ts_sorted)}')
    print(f'  Símbolo inicio: {start_symbol}')

    # Producciones de la gramática
    print('\n' + '─' * 60)
    print('  PRODUCCIONES')
    print('─' * 60)
    for nt in nts_sorted:
        for rule in productions[nt]:
            print(f'  {nt:8s} -> {" ".join(rule)}')

    # Req. 3 — Conjuntos PRIMERO
    print('\n' + '─' * 60)
    print('  CONJUNTOS PRIMERO')
    print('─' * 60)
    for nt in nts_sorted:
        print(f'  FIRST( {nt:6s} ) = {fmt_set(first[nt])}')

    # Req. 4 — Conjuntos SIGUIENTE
    print('\n' + '─' * 60)
    print('  CONJUNTOS SIGUIENTE')
    print('─' * 60)
    for nt in nts_sorted:
        print(f'  FOLLOW( {nt:6s} ) = {fmt_set(follow[nt])}')

    print_separator('═')


# =============================================================================
#   ENTRADA INTERACTIVA — menú y ejemplos predefinidos
# =============================================================================

# Ejemplos en formato texto (entrada manual)
EXAMPLES_TEXT = {
    '1': (
        "Expresión aritmética clásica (LL(1))",
        "E -> T E'\nE' -> + T E' | ε\nT -> F T'\nT' -> * F T' | ε\nF -> ( E ) | id"
    ),
    '2': (
        "Gramática simple con anulables",
        "S -> A B\nA -> a A | ε\nB -> b B | c"
    ),
    '3': (
        "Gramática con recursión por la izquierda",
        "S -> S a | A\nA -> b A c | b c"
    ),
}

# Ejemplos del  (formato dict, accesibles desde el menú)
EXAMPLES_DICT = {
    '4': ("Aritmética — formato dict ", GRAMMAR_DICT_1),
    '5': ("Anulables  — formato dict ", GRAMMAR_DICT_2),
}


def read_grammar_interactive() -> str:
    """Lee la gramática producción por producción; línea vacía termina."""
    print('\nEscribe las producciones (línea vacía para terminar):')
    print('  Formato : NT -> símbolo1 símbolo2 | alternativa')
    print('  Epsilon : ε  o  eps\n')
    lines = []
    while True:
        try:
            line = input('  > ')
        except EOFError:
            break
        if line.strip() == '':
            if lines:
                break
        else:
            lines.append(line)
    return '\n'.join(lines)


def process_and_print(productions, start_symbol, non_terminals, terminals):
    """Orquesta el cálculo de FIRST + FOLLOW y la impresión de resultados."""
    first  = compute_first(productions, non_terminals)
    follow = compute_follow(productions, non_terminals, start_symbol, first)
    print()
    print_results(productions, start_symbol, non_terminals, terminals,
                  first, follow)


def main():
    print_separator('═')
    print('  PRIMERO & SIGUIENTE — Calculadora de Gramáticas Libres de Contexto')
    print('  Diseño de Lenguajes de Programación 2026 · UVG')
    print_separator('═')

    while True:
        print('\n  Opciones:')
        for key, (name, _) in EXAMPLES_TEXT.items():
            print(f'    [{key}] Ejemplo (texto) : {name}')
        for key, (name, _) in EXAMPLES_DICT.items():
            print(f'    [{key}] Ejemplo (dict)  : {name}')
        print('    [0] Ingresar gramática manualmente')
        print('    [q] Salir')

        choice = input('\n  Selección: ').strip().lower()

        if choice == 'q':
            print('\n  ¡Hasta luego!\n')
            break

        try:
            if choice in EXAMPLES_TEXT:
                name, text = EXAMPLES_TEXT[choice]
                print(f'\n  Cargando: {name}')
                print_separator()
                for line in text.splitlines():
                    print(f'  {line}')
                productions, start_symbol, non_terminals, terminals = \
                    parse_grammar(text)
                process_and_print(productions, start_symbol,
                                  non_terminals, terminals)

            elif choice in EXAMPLES_DICT:
                name, gdict = EXAMPLES_DICT[choice]
                print(f'\n  Cargando: {name}')
                print_separator()
                productions, start_symbol, non_terminals, terminals = \
                    dict_to_productions(gdict)
                process_and_print(productions, start_symbol,
                                  non_terminals, terminals)

            elif choice == '0':
                text = read_grammar_interactive()
                if not text.strip():
                    print('  Gramática vacía, intenta de nuevo.')
                    continue
                productions, start_symbol, non_terminals, terminals = \
                    parse_grammar(text)
                process_and_print(productions, start_symbol,
                                  non_terminals, terminals)

            else:
                print('  Opción inválida.')
                continue

        except ValueError as e:
            print(f'\n  ⚠  Error: {e}')

        input('\n  [Enter para continuar]')


if __name__ == '__main__':
    main()
