"""
Dragons & IA — Datos iniciales (razas, clases, mundos).

Ejecutar con: python -m scripts.seed_data
"""

WORLDS = [
    {"id": "fantasia", "name": "Fantasía Medieval", "emoji": "🏰",
     "description": "Reinos, dragones, magia arcana y criaturas míticas."},
    {"id": "ciencia_ficcion", "name": "Ciencia Ficción", "emoji": "🚀",
     "description": "Naves espaciales, IAs rebeldes, megacorporaciones."},
    {"id": "isekai", "name": "Isekai", "emoji": "🌀",
     "description": "Transportado a otro mundo con tus conocimientos modernos."},
    {"id": "fantasia_oscura", "name": "Fantasía Oscura", "emoji": "💀",
     "description": "Horror, muerte, corrupción. La oscuridad acecha."},
]

RACES = [
    {"name": "Humano", "description": "Versátiles y ambiciosos. +1 a todas las stats."},
    {"name": "Elfo", "description": "Ágiles y longevos. +2 DES. Visión en la oscuridad."},
    {"name": "Enano", "description": "Resistentes y tenaces. +2 CON. Resistencia a venenos."},
    {"name": "Mediano", "description": "Pequeños y afortunados. +2 DES. Suerte natural."},
    {"name": "Tiefling", "description": "Herencia infernal. +2 CAR, +1 INT. Resistencia al fuego."},
    {"name": "Dracónido", "description": "Descendientes de dragones. +2 FUE, +1 CAR. Arma de aliento."},
    {"name": "Semielfo", "description": "Lo mejor de dos mundos. +2 CAR, +1 a dos stats."},
    {"name": "Semiorco", "description": "Fuerza bruta. +2 FUE, +1 CON. Resistencia implacable."},
    {"name": "Gnomo", "description": "Ingeniosos e inteligentes. +2 INT. Astucia gnómica."},
]

CLASSES = [
    {"name": "Guerrero", "hit_die": "d10",
     "description": "Maestro del combate. Experto en armas y armaduras."},
    {"name": "Mago", "hit_die": "d6",
     "description": "Estudioso de la magia arcana. Poderosos hechizos."},
    {"name": "Pícaro", "hit_die": "d8",
     "description": "Sigiloso y letal. Ataque furtivo y habilidades."},
    {"name": "Clérigo", "hit_die": "d8",
     "description": "Servidor divino. Curación y magia sagrada."},
    {"name": "Druida", "hit_die": "d8",
     "description": "Guardián de la naturaleza. Formas salvajes."},
    {"name": "Bardo", "hit_die": "d8",
     "description": "Artista y encantador. Inspiración y versatilidad."},
    {"name": "Paladín", "hit_die": "d10",
     "description": "Guerrero sagrado. Imposición de manos y auras."},
    {"name": "Ranger", "hit_die": "d10",
     "description": "Explorador y rastreador. Enemigo predilecto."},
    {"name": "Monje", "hit_die": "d8",
     "description": "Artista marcial. Ki y golpes devastadores."},
    {"name": "Hechicero", "hit_die": "d6",
     "description": "Magia innata. Metamagia para alterar hechizos."},
    {"name": "Brujo", "hit_die": "d8",
     "description": "Pacto oscuro. Magia de pacto y invocaciones."},
    {"name": "Bárbaro", "hit_die": "d12",
     "description": "Furia primitiva. Ira y resistencia sobrehumana."},
]

if __name__ == "__main__":
    import json

    data = {"worlds": WORLDS, "races": RACES, "classes": CLASSES}
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"\n✅ {len(WORLDS)} mundos, {len(RACES)} razas, {len(CLASSES)} clases disponibles.")
