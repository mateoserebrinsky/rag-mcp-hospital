| Encoder | Chunking | top-k | umbral | caída | recall | precision | context_relevance | archivo |
|---|---|---|---|---|---|---|---|---|
| multilingual-e5-base | ventanas 500/100 | 1 | 0 | - | 1.000 | 1.000 | **1.000** | `e5b__v500__k1` |
| multilingual-e5-base | secciones + título | 1 | 0 | - | 0.950 | 0.950 | **0.950** | `e5b__secmeta__k1` |
| paraphrase-multilingual-MiniLM-L12-v2 | secciones + título | 3 | 0 | 0.05 | 1.000 | 0.892 | **0.925** | `minilm__secmeta__k3__caida0.05` |
| multilingual-e5-base | ventanas 300/60 | 1 | 0 | - | 0.900 | 0.900 | **0.900** | `e5b__v300__k1` |
| multilingual-e5-small | secciones + título | 1 | 0 | - | 0.900 | 0.900 | **0.900** | `e5s__secmeta__k1` |
| paraphrase-multilingual-MiniLM-L12-v2 | secciones + título | 1 | 0 | - | 0.900 | 0.900 | **0.900** | `minilm__secmeta__k1` |
| paraphrase-multilingual-MiniLM-L12-v2 | secciones + título | 3 | 0.7 | - | 0.900 | 0.900 | **0.900** | `minilm__secmeta__k3__u0.7` |
| multilingual-e5-base | secciones | 1 | 0 | - | 0.850 | 0.850 | **0.850** | `e5b__sec__k1` |
| paraphrase-multilingual-MiniLM-L12-v2 | secciones + título | 3 | 0 | 0.1 | 1.000 | 0.750 | **0.825** | `minilm__secmeta__k3__caida0.1` |
| multilingual-e5-small | secciones | 1 | 0 | - | 0.800 | 0.800 | **0.800** | `e5s__sec__k1` |
| multilingual-e5-small | ventanas 500/100 | 1 | 0 | - | 0.800 | 0.800 | **0.800** | `e5s__v500__k1` |
| paraphrase-multilingual-MiniLM-L12-v2 | secciones + título | 3 | 0.5 | - | 1.000 | 0.692 | **0.775** | `minilm__secmeta__k3__u0.5` |
| paraphrase-multilingual-MiniLM-L12-v2 | secciones | 1 | 0 | - | 0.700 | 0.700 | **0.700** | `minilm__sec__k1` |
| paraphrase-multilingual-MiniLM-L12-v2 | secciones | 3 | 0.7 | - | 0.700 | 0.700 | **0.700** | `minilm__sec__k3__u0.7` |
| paraphrase-multilingual-MiniLM-L12-v2 | ventanas 300/60 | 1 | 0 | - | 0.700 | 0.700 | **0.700** | `minilm__v300__k1` |
| paraphrase-multilingual-MiniLM-L12-v2 | ventanas 300/60 | 3 | 0.7 | - | 0.700 | 0.700 | **0.700** | `minilm__v300__k3__u0.7` |
| multilingual-e5-base | secciones + título | 3 | 0 | 0.05 | 1.000 | 0.583 | **0.692** | `e5b__secmeta__k3__caida0.05` |
| multilingual-e5-small | secciones + título | 3 | 0 | 0.05 | 1.000 | 0.583 | **0.692** | `e5s__secmeta__k3__caida0.05` |
| multilingual-e5-base | ventanas 500/100 | 2 | 0 | - | 1.000 | 0.525 | **0.683** | `e5b__v500__k2` |
| paraphrase-multilingual-MiniLM-L12-v2 | ventanas 300/60 | 3 | 0 | 0.05 | 0.800 | 0.633 | **0.683** | `minilm__v300__k3__caida0.05` |
| paraphrase-multilingual-MiniLM-L12-v2 | ventanas 500/100 | 3 | 0 | 0.05 | 0.800 | 0.633 | **0.683** | `minilm__v500__k3__caida0.05` |
| multilingual-e5-base | secciones + título | 2 | 0 | - | 1.000 | 0.500 | **0.667** | `e5b__secmeta__k2` |
| paraphrase-multilingual-MiniLM-L12-v2 | secciones + título | 2 | 0 | - | 1.000 | 0.500 | **0.667** | `minilm__secmeta__k2` |
| paraphrase-multilingual-MiniLM-L12-v2 | ventanas 300/60 | 3 | 0 | 0.1 | 0.850 | 0.583 | **0.665** | `minilm__v300__k3__caida0.1` |
| paraphrase-multilingual-MiniLM-L12-v2 | secciones | 3 | 0 | 0.05 | 0.750 | 0.617 | **0.658** | `minilm__sec__k3__caida0.05` |
| multilingual-e5-small | ventanas 300/60 | 1 | 0 | - | 0.650 | 0.650 | **0.650** | `e5s__v300__k1` |
| paraphrase-multilingual-MiniLM-L12-v2 | ventanas 500/100 | 1 | 0 | - | 0.650 | 0.650 | **0.650** | `minilm__v500__k1` |
| paraphrase-multilingual-MiniLM-L12-v2 | ventanas 500/100 | 3 | 0.7 | - | 0.650 | 0.650 | **0.650** | `minilm__v500__k3__u0.7` |
| paraphrase-multilingual-MiniLM-L12-v2 | ventanas 500/100 | 3 | 0 | 0.1 | 0.850 | 0.567 | **0.642** | `minilm__v500__k3__caida0.1` |
| multilingual-e5-base | ventanas 300/60 | 2 | 0 | - | 0.950 | 0.475 | **0.633** | `e5b__v300__k2` |
| multilingual-e5-small | secciones + título | 2 | 0 | - | 0.950 | 0.475 | **0.633** | `e5s__secmeta__k2` |
| paraphrase-multilingual-MiniLM-L12-v2 | secciones | 3 | 0.5 | - | 0.800 | 0.558 | **0.625** | `minilm__sec__k3__u0.5` |
| multilingual-e5-small | ventanas 500/100 | 2 | 0 | - | 0.900 | 0.475 | **0.617** | `e5s__v500__k2` |
| paraphrase-multilingual-MiniLM-L12-v2 | secciones | 3 | 0 | 0.1 | 0.800 | 0.550 | **0.617** | `minilm__sec__k3__caida0.1` |
| paraphrase-multilingual-MiniLM-L12-v2 | ventanas 300/60 | 3 | 0.5 | - | 0.850 | 0.533 | **0.617** | `minilm__v300__k3__u0.5` |
| multilingual-e5-base | ventanas 500/100 | 3 | 0 | 0.05 | 1.000 | 0.475 | **0.613** | `e5b__v500__k3__caida0.05` |
| multilingual-e5-base | secciones | 2 | 0 | - | 0.900 | 0.450 | **0.600** | `e5b__sec__k2` |
| paraphrase-multilingual-MiniLM-L12-v2 | ventanas 500/100 | 3 | 0.5 | - | 0.750 | 0.525 | **0.590** | `minilm__v500__k3__u0.5` |
| multilingual-e5-small | secciones | 2 | 0 | - | 0.850 | 0.425 | **0.567** | `e5s__sec__k2` |
| paraphrase-multilingual-MiniLM-L12-v2 | secciones | 2 | 0 | - | 0.850 | 0.425 | **0.567** | `minilm__sec__k2` |
| paraphrase-multilingual-MiniLM-L12-v2 | ventanas 300/60 | 2 | 0 | - | 0.850 | 0.425 | **0.567** | `minilm__v300__k2` |
| multilingual-e5-base | secciones | 3 | 0 | 0.05 | 0.900 | 0.442 | **0.558** | `e5b__sec__k3__caida0.05` |
| paraphrase-multilingual-MiniLM-L12-v2 | ventanas 500/100 | 2 | 0 | - | 0.800 | 0.425 | **0.550** | `minilm__v500__k2` |
| multilingual-e5-small | ventanas 300/60 | 3 | 0 | 0.05 | 0.950 | 0.400 | **0.542** | `e5s__v300__k3__caida0.05` |
| multilingual-e5-base | ventanas 500/100 | 3 | 0 | 0.1 | 1.000 | 0.375 | **0.538** | `e5b__v500__k3__caida0.1` |
| multilingual-e5-base | ventanas 300/60 | 3 | 0 | 0.05 | 0.950 | 0.392 | **0.533** | `e5b__v300__k3__caida0.05` |
| multilingual-e5-small | ventanas 300/60 | 2 | 0 | - | 0.800 | 0.400 | **0.533** | `e5s__v300__k2` |
| multilingual-e5-base | ventanas 500/100 | 3 | 0 | - | 1.000 | 0.367 | **0.530** | `e5b__v500__k3` |
| multilingual-e5-base | ventanas 500/100 | 3 | 0.5 | - | 1.000 | 0.367 | **0.530** | `e5b__v500__k3__u0.5` |
| multilingual-e5-base | ventanas 500/100 | 3 | 0.7 | - | 1.000 | 0.367 | **0.530** | `e5b__v500__k3__u0.7` |
| multilingual-e5-small | secciones | 3 | 0 | 0.05 | 0.900 | 0.400 | **0.525** | `e5s__sec__k3__caida0.05` |
| multilingual-e5-small | ventanas 500/100 | 3 | 0 | 0.05 | 0.950 | 0.375 | **0.523** | `e5s__v500__k3__caida0.05` |
| multilingual-e5-base | secciones + título | 3 | 0 | - | 1.000 | 0.333 | **0.500** | `e5b__secmeta__k3` |
| multilingual-e5-base | secciones + título | 3 | 0 | 0.1 | 1.000 | 0.333 | **0.500** | `e5b__secmeta__k3__caida0.1` |
| multilingual-e5-base | secciones + título | 3 | 0.5 | - | 1.000 | 0.333 | **0.500** | `e5b__secmeta__k3__u0.5` |
| multilingual-e5-base | secciones + título | 3 | 0.7 | - | 1.000 | 0.333 | **0.500** | `e5b__secmeta__k3__u0.7` |
| multilingual-e5-small | secciones + título | 3 | 0 | - | 1.000 | 0.333 | **0.500** | `e5s__secmeta__k3` |
| multilingual-e5-small | secciones + título | 3 | 0 | 0.1 | 1.000 | 0.333 | **0.500** | `e5s__secmeta__k3__caida0.1` |
| multilingual-e5-small | secciones + título | 3 | 0.5 | - | 1.000 | 0.333 | **0.500** | `e5s__secmeta__k3__u0.5` |
| multilingual-e5-small | secciones + título | 3 | 0.7 | - | 1.000 | 0.333 | **0.500** | `e5s__secmeta__k3__u0.7` |
| paraphrase-multilingual-MiniLM-L12-v2 | secciones + título | 3 | 0 | - | 1.000 | 0.333 | **0.500** | `minilm__secmeta__k3` |
| multilingual-e5-small | ventanas 500/100 | 3 | 0 | - | 0.950 | 0.333 | **0.490** | `e5s__v500__k3` |
| multilingual-e5-small | ventanas 500/100 | 3 | 0 | 0.1 | 0.950 | 0.333 | **0.490** | `e5s__v500__k3__caida0.1` |
| multilingual-e5-small | ventanas 500/100 | 3 | 0.5 | - | 0.950 | 0.333 | **0.490** | `e5s__v500__k3__u0.5` |
| multilingual-e5-small | ventanas 500/100 | 3 | 0.7 | - | 0.950 | 0.333 | **0.490** | `e5s__v500__k3__u0.7` |
| multilingual-e5-base | ventanas 300/60 | 3 | 0 | 0.1 | 0.950 | 0.325 | **0.483** | `e5b__v300__k3__caida0.1` |
| multilingual-e5-base | ventanas 300/60 | 3 | 0 | - | 0.950 | 0.317 | **0.475** | `e5b__v300__k3` |
| multilingual-e5-base | ventanas 300/60 | 3 | 0.5 | - | 0.950 | 0.317 | **0.475** | `e5b__v300__k3__u0.5` |
| multilingual-e5-base | ventanas 300/60 | 3 | 0.7 | - | 0.950 | 0.317 | **0.475** | `e5b__v300__k3__u0.7` |
| multilingual-e5-small | ventanas 300/60 | 3 | 0 | - | 0.950 | 0.317 | **0.475** | `e5s__v300__k3` |
| multilingual-e5-small | ventanas 300/60 | 3 | 0 | 0.1 | 0.950 | 0.317 | **0.475** | `e5s__v300__k3__caida0.1` |
| multilingual-e5-small | ventanas 300/60 | 3 | 0.5 | - | 0.950 | 0.317 | **0.475** | `e5s__v300__k3__u0.5` |
| multilingual-e5-small | ventanas 300/60 | 3 | 0.7 | - | 0.950 | 0.317 | **0.475** | `e5s__v300__k3__u0.7` |
| paraphrase-multilingual-MiniLM-L12-v2 | ventanas 500/100 | 3 | 0 | - | 0.900 | 0.317 | **0.465** | `minilm__v500__k3` |
| multilingual-e5-base | secciones | 3 | 0 | 0.1 | 0.900 | 0.308 | **0.458** | `e5b__sec__k3__caida0.1` |
| multilingual-e5-base | secciones | 3 | 0 | - | 0.900 | 0.300 | **0.450** | `e5b__sec__k3` |
| multilingual-e5-base | secciones | 3 | 0.5 | - | 0.900 | 0.300 | **0.450** | `e5b__sec__k3__u0.5` |
| multilingual-e5-base | secciones | 3 | 0.7 | - | 0.900 | 0.300 | **0.450** | `e5b__sec__k3__u0.7` |
| multilingual-e5-small | secciones | 3 | 0 | - | 0.900 | 0.300 | **0.450** | `e5s__sec__k3` |
| multilingual-e5-small | secciones | 3 | 0 | 0.1 | 0.900 | 0.300 | **0.450** | `e5s__sec__k3__caida0.1` |
| multilingual-e5-small | secciones | 3 | 0.5 | - | 0.900 | 0.300 | **0.450** | `e5s__sec__k3__u0.5` |
| multilingual-e5-small | secciones | 3 | 0.7 | - | 0.900 | 0.300 | **0.450** | `e5s__sec__k3__u0.7` |
| paraphrase-multilingual-MiniLM-L12-v2 | secciones | 3 | 0 | - | 0.900 | 0.300 | **0.450** | `minilm__sec__k3` |
| paraphrase-multilingual-MiniLM-L12-v2 | ventanas 300/60 | 3 | 0 | - | 0.850 | 0.300 | **0.440** | `minilm__v300__k3` |
| multilingual-e5-base | ventanas 500/100 | 5 | 0 | - | 1.000 | 0.220 | **0.357** | `e5b__v500__k5` |
| multilingual-e5-base | secciones + título | 5 | 0 | - | 1.000 | 0.200 | **0.333** | `e5b__secmeta__k5` |
| multilingual-e5-small | secciones + título | 5 | 0 | - | 1.000 | 0.200 | **0.333** | `e5s__secmeta__k5` |
| paraphrase-multilingual-MiniLM-L12-v2 | secciones + título | 5 | 0 | - | 1.000 | 0.200 | **0.333** | `minilm__secmeta__k5` |
| multilingual-e5-base | ventanas 300/60 | 5 | 0 | - | 0.950 | 0.200 | **0.329** | `e5b__v300__k5` |
| multilingual-e5-small | ventanas 300/60 | 5 | 0 | - | 0.950 | 0.200 | **0.329** | `e5s__v300__k5` |
| multilingual-e5-small | ventanas 500/100 | 5 | 0 | - | 0.950 | 0.200 | **0.329** | `e5s__v500__k5` |
| paraphrase-multilingual-MiniLM-L12-v2 | ventanas 500/100 | 5 | 0 | - | 0.900 | 0.200 | **0.324** | `minilm__v500__k5` |
| multilingual-e5-base | secciones | 5 | 0 | - | 0.950 | 0.190 | **0.317** | `e5b__sec__k5` |
| paraphrase-multilingual-MiniLM-L12-v2 | secciones | 5 | 0 | - | 0.950 | 0.190 | **0.317** | `minilm__sec__k5` |
| BERT multilingüe (línea de base) | secciones + título | 1 | 0 | - | 0.300 | 0.300 | **0.300** | `bert__secmeta__k1` |
| BERT multilingüe (línea de base) | secciones + título | 3 | 0.7 | - | 0.300 | 0.300 | **0.300** | `bert__secmeta__k3__u0.7` |
| multilingual-e5-small | secciones | 5 | 0 | - | 0.900 | 0.180 | **0.300** | `e5s__sec__k5` |
| paraphrase-multilingual-MiniLM-L12-v2 | ventanas 300/60 | 5 | 0 | - | 0.850 | 0.180 | **0.295** | `minilm__v300__k5` |
| BERT multilingüe (línea de base) | secciones | 3 | 0.7 | - | 0.300 | 0.275 | **0.283** | `bert__sec__k3__u0.7` |
| BERT multilingüe (línea de base) | secciones | 1 | 0 | - | 0.250 | 0.250 | **0.250** | `bert__sec__k1` |
| BERT multilingüe (línea de base) | ventanas 500/100 | 1 | 0 | - | 0.250 | 0.250 | **0.250** | `bert__v500__k1` |
| BERT multilingüe (línea de base) | ventanas 500/100 | 3 | 0.7 | - | 0.250 | 0.250 | **0.250** | `bert__v500__k3__u0.7` |
| BERT multilingüe (línea de base) | secciones + título | 2 | 0 | - | 0.350 | 0.175 | **0.233** | `bert__secmeta__k2` |
| BERT multilingüe (línea de base) | ventanas 500/100 | 2 | 0 | - | 0.350 | 0.175 | **0.233** | `bert__v500__k2` |
| BERT multilingüe (línea de base) | secciones + título | 3 | 0 | 0.05 | 0.350 | 0.158 | **0.208** | `bert__secmeta__k3__caida0.05` |
| BERT multilingüe (línea de base) | secciones | 2 | 0 | - | 0.300 | 0.150 | **0.200** | `bert__sec__k2` |
| BERT multilingüe (línea de base) | secciones | 3 | 0 | 0.05 | 0.350 | 0.150 | **0.200** | `bert__sec__k3__caida0.05` |
| BERT multilingüe (línea de base) | ventanas 500/100 | 3 | 0 | - | 0.350 | 0.133 | **0.190** | `bert__v500__k3` |
| BERT multilingüe (línea de base) | ventanas 500/100 | 3 | 0 | 0.05 | 0.350 | 0.133 | **0.190** | `bert__v500__k3__caida0.05` |
| BERT multilingüe (línea de base) | ventanas 500/100 | 3 | 0 | 0.1 | 0.350 | 0.133 | **0.190** | `bert__v500__k3__caida0.1` |
| BERT multilingüe (línea de base) | ventanas 500/100 | 3 | 0.5 | - | 0.350 | 0.133 | **0.190** | `bert__v500__k3__u0.5` |
| BERT multilingüe (línea de base) | secciones + título | 3 | 0 | - | 0.350 | 0.117 | **0.175** | `bert__secmeta__k3` |
| BERT multilingüe (línea de base) | secciones + título | 3 | 0 | 0.1 | 0.350 | 0.117 | **0.175** | `bert__secmeta__k3__caida0.1` |
| BERT multilingüe (línea de base) | secciones + título | 3 | 0.5 | - | 0.350 | 0.117 | **0.175** | `bert__secmeta__k3__u0.5` |
| BERT multilingüe (línea de base) | secciones | 3 | 0 | - | 0.350 | 0.117 | **0.175** | `bert__sec__k3` |
| BERT multilingüe (línea de base) | secciones | 3 | 0 | 0.1 | 0.350 | 0.117 | **0.175** | `bert__sec__k3__caida0.1` |
| BERT multilingüe (línea de base) | secciones | 3 | 0.5 | - | 0.350 | 0.117 | **0.175** | `bert__sec__k3__u0.5` |
| BERT multilingüe (línea de base) | ventanas 300/60 | 3 | 0 | - | 0.350 | 0.117 | **0.175** | `bert__v300__k3` |
| BERT multilingüe (línea de base) | ventanas 300/60 | 3 | 0 | 0.05 | 0.300 | 0.133 | **0.175** | `bert__v300__k3__caida0.05` |
| BERT multilingüe (línea de base) | ventanas 300/60 | 3 | 0 | 0.1 | 0.350 | 0.117 | **0.175** | `bert__v300__k3__caida0.1` |
| BERT multilingüe (línea de base) | ventanas 300/60 | 3 | 0.5 | - | 0.350 | 0.117 | **0.175** | `bert__v300__k3__u0.5` |
| BERT multilingüe (línea de base) | secciones + título | 5 | 0 | - | 0.500 | 0.100 | **0.167** | `bert__secmeta__k5` |
| BERT multilingüe (línea de base) | ventanas 300/60 | 2 | 0 | - | 0.250 | 0.125 | **0.167** | `bert__v300__k2` |
| BERT multilingüe (línea de base) | ventanas 500/100 | 5 | 0 | - | 0.400 | 0.100 | **0.157** | `bert__v500__k5` |
| BERT multilingüe (línea de base) | secciones | 5 | 0 | - | 0.450 | 0.090 | **0.150** | `bert__sec__k5` |
| BERT multilingüe (línea de base) | ventanas 300/60 | 5 | 0 | - | 0.400 | 0.080 | **0.133** | `bert__v300__k5` |
| BERT multilingüe (línea de base) | ventanas 300/60 | 3 | 0.7 | - | 0.150 | 0.117 | **0.125** | `bert__v300__k3__u0.7` |
| BERT multilingüe (línea de base) | ventanas 300/60 | 1 | 0 | - | 0.100 | 0.100 | **0.100** | `bert__v300__k1` |
