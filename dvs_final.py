import math

INFINITY = math.inf

def initialize_routing_tables(network):
    """
    Inizializza le tabelle di routing per ogni nodo.
    Ogni tabella contiene sia il costo sia il next hop per raggiungere ogni destinazione.
    """
    tables = {}
    for node in network:
        tables[node] = {}
        for dest in network:
            if node == dest:
                # Distanza a sé stesso è 0, nessun next hop necessario
                tables[node][dest] = (0, None)
            elif dest in network[node]:
                # Distanza ai vicini diretti
                tables[node][dest] = (network[node][dest], dest)
            else:
                # Destinazioni non raggiungibili direttamente
                tables[node][dest] = (INFINITY, None)
    return tables

def update_routing_table(tables, network):
    """
    Aggiorna le tabelle di routing utilizzando l'algoritmo Distance Vector,
    aggiornando sia il costo sia il next hop.
    """
    updated = False
    for node in network:
        for neighbor, cost_to_neighbor in network[node].items():
            for dest, (neighbor_to_dest_cost, _) in tables[neighbor].items():
                new_cost = cost_to_neighbor + neighbor_to_dest_cost
                current_cost, current_hop = tables[node][dest]
                if new_cost < current_cost:
                    # Aggiorna costo e next hop
                    tables[node][dest] = (new_cost, neighbor)
                    updated = True
    return updated

def simulate_routing(network, max_iterations=100):
    """
    Simula il protocollo di routing Distance Vector fino alla convergenza,
    mostrando sia i costi sia i next hop.
    """
    tables = initialize_routing_tables(network)
    iteration = 0

    while iteration < max_iterations:
        print(f"\nIterazione {iteration + 1}")
        for node, table in tables.items():
            print(f"Tabella di routing per {node}:")
            print(f"{'Destinazione':<12}{'Costo':<10}{'Next Hop':<10}")
            for dest, (cost, hop) in sorted(table.items()):
                cost_display = f"{cost}" if cost != INFINITY else "∞"
                hop_display = hop if hop is not None else "-"
                print(f"{dest:<12}{cost_display:<10}{hop_display:<10}")
        print()

        updated = update_routing_table(tables, network)
        if not updated:
            print("Convergenza raggiunta!")
            break
        iteration += 1

    if iteration == max_iterations:
        print("Limite massimo di iterazioni raggiunto. La rete potrebbe non essere convergente.")

    return tables

if __name__ == "__main__":
    # Test Network 1: Random
    network = {
        'A': {'B': 1, 'C': 4},
        'B': {'A': 1, 'C': 2, 'D': 6},
        'C': {'A': 4, 'B': 2, 'D': 3},
        'D': {'B': 6, 'C': 3}
    }

    final_tables = simulate_routing(network)
    print("\nTabella di routing finale:")
    for node, table in final_tables.items():
        print(f"{node}:")
        print(f"{'Destinazione':<12}{'Costo':<10}{'Next Hop':<10}")
        for dest, (cost, hop) in sorted(table.items()):
            cost_display = f"{cost}" if cost != INFINITY else "∞"
            hop_display = hop if hop is not None else "-"
            print(f"{dest:<12}{cost_display:<10}{hop_display:<10}")
