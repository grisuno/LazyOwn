import os
import glob
import yaml
import networkx as nx
import polars as pl
from pyvis.network import Network

def generate_graphs():
    atomic_path = os.path.join("external", ".exploit", "atomic-red-team", "atomics")
    yaml_files = glob.glob(os.path.join(atomic_path, "**", "*.yaml"), recursive=True)
    tests = []

    for file in yaml_files:
        with open(file, "r") as f:
            data = yaml.safe_load(f)
            if "atomic_tests" in data:
                for test in data["atomic_tests"]:
                    test_id = test["auto_generated_guid"]
                    tests.append({
                        "id": test_id,
                        "name": test["name"],
                        "description": test.get("description", "No description available"),
                        "platforms": test.get("supported_platforms", []),
                        "command": test.get("executor", {}).get("command", "No command available"),
                        "prereq_command": test.get("dependencies", [{}])[0].get("prereq_command", ""),
                        "get_prereq_command": test.get("dependencies", [{}])[0].get("get_prereq_command", ""),
                        "cleanup_command": test.get("executor", {}).get("cleanup_command", ""),
                        "input_arguments": test.get("input_arguments", {}),
                        "mitre_id": data.get("attack_technique", "No MITRE ID available")
                    })

    # Convertir la lista de pruebas en un DataFrame de Polars
    df = pl.DataFrame(tests)

    # Guardar el DataFrame en un archivo Parquet
    df.write_parquet("tests.parquet")

    # Crear un grafo dirigido
    G = nx.DiGraph()

    for test_info in tests:
        test_id = test_info['id']
        node_label = f"{test_info['name']} ({test_info['id']})"
        G.add_node(test_id, title=test_id, label=node_label, shape='image', image='/static/c2.png')

    net = Network(height="750px", width="100%", bgcolor="#6c757d", font_color="#f8f9fa")
    net.from_nx(G)

    # Añadir JavaScript para copiar el ID del nodo seleccionado
    js_code = """
    <script type="text/javascript">
      network.on("selectNode", function(params) {
        if (params.nodes.length > 0) {
          var selectedNodeId = params.nodes[0];
          console.log("Nodo seleccionado: " + selectedNodeId);
          navigator.clipboard.writeText(selectedNodeId);
        }
      });
    </script>
    """

    # Guardar en la carpeta templates
    net.save_graph("templates/graph.html")

    # Añadir el JavaScript al HTML generado
    with open("templates/graph.html", "a") as file:
        file.write(js_code)

if __name__ == "__main__":
    generate_graphs()