import requests
import time
import sys
import os
# === CONFIGURACIÓN ===
# Usa tu token si lo tienes (opcional, pero recomendado)
TOKEN = ""  # Deja vacío si no quieres autenticarte

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
} if TOKEN else {}

# === FUNCIÓN: Buscar repos nuevos ===
def buscar_repos_nuevos(
    lenguaje="python",
    dias=1,
    cantidad=100,
    orden="desc"
):
    # Calcular fecha mínima
    desde = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ",
        time.gmtime(time.time() - dias * 86400)
    )

    # Construir query
    query = f"created:>={desde} language:{lenguaje}"
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "created",
        "order": orden,
        "per_page": min(cantidad, 100)  # Máximo por página: 100
    }

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        print("Error en la API:", response.status_code, response.json())
        return []

    data = response.json()
    repos = data.get("items", [])

    # Extraer solo los campos que te interesan
    resultado = []
    for repo in repos:
        info = {
            "nombre": repo["name"],
            "owner": repo["owner"]["login"],
            "url": repo["html_url"],
            "descripcion": repo["description"] or "No description",
            "lenguaje": repo["language"],
            "estrellas": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "creado": repo["created_at"],
            "tamaño_kb": f"{repo['size']} KB",
            "licencia": repo["license"]["name"] if repo["license"] else "no licence"
        }
        resultado.append(info)

    return resultado

# === USO: Obtener repos nuevos de Python en las últimas 24h ===
if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg1 = sys.argv[1]
    else:
        arg1 = "python"

    print("Searching new repos...\n")
    repos = buscar_repos_nuevos(lenguaje=arg1, dias=1, cantidad=30)
    sys.stdout = open('output.txt', 'w')
    for i, repo in enumerate(repos, 1):
        print(f"{i}. {repo['nombre']} (@{repo['owner']})")
        print(f"   🌐 {repo['url']}")
        print(f"   📝 {repo['descripcion']}")
        print(f"   💻 Lang: {repo['lenguaje']}")
        print(f"   ⭐ Stars: {repo['estrellas']} | 🔄 Forks: {repo['forks']}")
        print(f"   📅 Created: {repo['creado'][:10]} | 📦 Tamaño: {repo['tamaño_kb']}")
        print(f"   📄 Licence: {repo['licencia']}")
        print("-" * 60)
    sys.stdout.close()
    os.system("cat output.txt | gum format")
