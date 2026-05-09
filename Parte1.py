EPSILON = 'ε'
DOLLAR  = '$'


# GRAMÁTICAS DE PRUEBA

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



# TERMINALES

def get_terminals(grammar: dict) -> set:
    non_terminals = set(grammar.keys())
    terminals = set()

    for productions in grammar.values():
        for prod in productions:
            for symbol in prod.split():
                if symbol not in non_terminals and symbol != EPSILON:
                    terminals.add(symbol)

    return terminals

# FIRST

def first_of_string(symbols: list,
                    first:   dict,
                    non_terminals: set) -> set:
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
                break      
        else:
            result.add(sym) # terminal ordinario
            break
    else:
        # todos los símbolos de la cadena pueden derivar ε
        result.add(EPSILON)

    return result


def compute_first(productions:   dict,
                  non_terminals: set) -> dict[str, set]:
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
    productions, _, non_terminals, _ = dict_to_productions(grammar_dict)
    return compute_first(productions, non_terminals)
