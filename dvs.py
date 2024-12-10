import math

INFINITY = math.inf

def initialize_routing_table(node_labels):
    """Inizializza la tabella di routing per ogni nodo con distanza e next hop."""
    num_nodes = len(node_labels)
    return [
        {node_labels[j]: (0 if i == j else INFINITY, None) for j in range(num_nodes)}
        for i in range(num_nodes)
    ]

def validate_network(network):
    """Verifica che la matrice di rete sia valida."""
    num_nodes = len(network)
    if any(len(row) != num_nodes for row in network):
        raise ValueError("La matrice di adiacenza deve essere quadrata.")
    if any(c < 0 and c != INFINITY for row in network for c in row):
        raise ValueError("I costi devono essere non negativi o INFINITY.")

def update_routing_table(node, tables, network, node_labels):
    """Aggiorna la tabella di routing di un nodo basandosi sulle tabelle dei vicini."""
    updated = False
    for dest_idx, dest_label in enumerate(node_labels):
        if dest_idx == node:
            continue
        min_distance, next_hop = tables[node][dest_label]
        for neighbor_idx, neighbor_label in enumerate(node_labels):
            if network[node][neighbor_idx] == INFINITY or neighbor_idx == node:
                continue
            # Nuova distanza calcolata tramite il vicino
            new_distance = network[node][neighbor_idx] + tables[neighbor_idx][dest_label][0]
            if new_distance < min_distance:
                min_distance, next_hop = new_distance, neighbor_label
                updated = True
        tables[node][dest_label] = (min_distance, next_hop)
    return updated

def print_routing_tables(tables, node_labels):
    """Stampa le tabelle di routing di tutti i nodi."""
    for node_idx, table in enumerate(tables):
        node_label = node_labels[node_idx]
        print(f"\nTabella di routing per il nodo {node_label}:")
        print(f"{'Destinazione':<12}{'Distanza':<10}{'Next Hop':<10}")
        for dest, (dist, hop) in table.items():
            dist_display = f"{dist}" if dist != INFINITY else "∞"
            hop_display = hop if hop is not None else "None"
            print(f"{dest:<12}{dist_display:<10}{hop_display:<10}")
    print()

def simulate_distance_vector(network, node_labels):
    """Simula il protocollo Distance Vector Routing e restituisce le tabelle finali."""
    validate_network(network)
    num_nodes = len(network)
    tables = initialize_routing_table(node_labels)

    print("Stato iniziale delle tabelle di routing:")
    print_routing_tables(tables, node_labels)

    iteration = 0
    while True:
        print(f"\nIterazione {iteration + 1}:")
        updated = any(update_routing_table(node, tables, network, node_labels) for node in range(num_nodes))
        print_routing_tables(tables, node_labels)
        if not updated:
            break
        iteration += 1

    print("Convergenza raggiunta!")
    return tables

# Definizione della rete (esempio: matrice di adiacenza)
network = [
    [0, 1, 4, INFINITY],
    [1, 0, 2, 6],
    [4, 2, 0, 3],
    [INFINITY, 6, 3, 0]
]

# Etichette dei nodi
node_labels = ['A', 'B', 'C', 'D']

simulate_distance_vector(network, node_labels)
