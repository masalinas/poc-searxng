# Description
PoC SearXNG is a free internet metasearch engine.

## Categories support by SearXNG
- general: Es la categoría por defecto. Busca en motores web tradicionales como Google, Bing, DuckDuckGo, Qwant y Wikipedia.

- science (Ciencia): Ideal para tu investigación. Modula la búsqueda hacia repositorios académicos como arXiv, Google Scholar, PubMed, Crossref, BASE y Semantic Scholar.

- it (Informática / Tecnología): Especializada en desarrollo. Consulta plataformas como GitHub, GitLab, Stack Overflow, PyPI (Python Package Index), Arch Linux y la documentación de diferentes distribuciones o lenguajes.

- images (Imágenes): Busca contenido visual a través de Google Images, Bing Images, Flickr, Pinterest o Pixabay.

- videos: Filtra contenido multimedia en plataformas como YouTube, Vimeo, Dailymotion o PeerTube.

- news (Noticias): Agrupa fuentes de actualidad y prensa global, extrayendo artículos recientes de Google News, Yahoo News, o feeds RSS de medios de comunicación.

- map (Mapas/Geolocalización): Utiliza servicios como OpenStreetMap, Photon o buscadores de direcciones para devolver coordenadas y mapas.

- music (Música): Filtra en plataformas de streaming de audio y bases de datos musicales como SoundCloud, Bandcamp o Genius.

- social_media (Redes Sociales): Escanea plataformas comunitarias y de microblogging (como Reddit, Mastodon o lemmy).

- files (Archivos): Diseñado para buscar descargas de archivos específicos, torrents o distribuciones de software.

## configure searxng
Create default folder for configuration and data volumes:

```shell
$ mkdir -p ./searxng/config/ ./searxng/data/
$ cd ./searxng/
```

Create a default secret_key for searxng
```shell
$ openssl rand -hex 32
52d5a2c1f28adf38e0bb182b6c53079fd09811523299cedbfd0b7dd8a5488f9
```

Create a new settings.yml file under `./searxng/config/` with this information. This file inherits the default searxng configuration
and add our custom ones:

```shell
# Read the documentation before extending the defaults:
# https://docs.searxng.org/admin/settings/

use_default_settings: true

server:
  port: 8080
  bind_address: "0.0.0.0"
  secret_key: "52d5a2c1f28adf38e0bb182b6c53079fd09811523299cedbfd0b7dd8a5488f9f"

# 2. Configuración global de las búsquedas y formatos requeridos
search:
  safe_search: 0
  autocomplete: ""
  formats:
    - html
    - json
```

## Start from docker
```shell
$ docker run --name searxng -d \
    -p 8888:8080 \
    -v "./config/:/etc/searxng/" \
    -v "./data/:/var/cache/searxng/" \
    docker.io/searxng/searxng:latest
```

## Check configuration
```shell
curl "http://localhost:8888/search?q=test&format=json"
```

## Test searxng
$ python main.py 

/home/miguel/git/poc-searxng/main.py:1: DeprecationWarning: `langchain-community` is being sunset and is no longer actively maintained. See https://github.com/langchain-ai/langchain-community/issues/674 for details and migration guidance toward standalone integration packages.
  from langchain_community.utilities import SearxSearchWrapper
--- Result 1 ---
Title: MAF-Net: A multimodal data fusion approach for human action recognition
Link:  https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0319656
Engines Used: ['google scholar']
Snippet: … for data preparation, feature extraction, and model design in our multimodal human activity recognition … both RGB and skeletal data to enhance recognition accuracy and robustness. By …

--- Result 2 ---
Title: RGB video and inertial sensing fusion method for human action recognition in human-robot collaborative manufacturing
Link:  https://www.sciencedirect.com/science/article/pii/S0278612525002341
Engines Used: ['google scholar']
Snippet: … fusion strategies of two modalities are studied: decision-level fusion and feature-level fusion… assembly as an example, a multi-modal human assembly action dataset for HAR (HAAD-…

--- Result 3 ---
Title: Multimodal feature fusion for human activity recognition using human centric temporal transformer
Link:  https://www.sciencedirect.com/science/article/pii/S0952197625018469
Engines Used: ['google scholar']
Snippet: In recent years, human activity recognition (HAR) has focused considerable interest due to its manifold monitoring applications. Mainstream HAR approaches often face challenges with …

--- Result 4 ---
Title: Advancing activity recognition with multimodal fusion and transformer techniques
Link:  https://ieeexplore.ieee.org/abstract/document/10955127/
Engines Used: ['google scholar']
Snippet: … that markedly improves activity recognition by combining multimodal sensor fusion with a … In this study, we introduce an advanced methodology for Human Activity Recognition (HAR) …

--- Result 5 ---
Title: Distilled mid-fusion transformer networks for multi-modal human activity recognition
Link:  https://www.sciencedirect.com/science/article/pii/S0950705125012018
Engines Used: ['google scholar']
Snippet: … various sensors, Multi-modal Human Activity Recognition can … , their potential in extracting salient multi-modal spatial-temporal … Additionally, reducing the complexity of the multi-modal …

## Some links

- [SearXNG Docker Docs](https://docs.searxng.org/admin/installation-docker.html)
- [SearXNG Langchain Community](https://reference.langchain.com/python/langchain-community/utilities/searx_search)
- [SearXNG Search Engines](https://docs.searxng.org/user/configured_engines.html#configured-engines)
