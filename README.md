# InstructLLM

Ein einfaches Beispiel für ein instruktionsbasiertes Language Model mit Python und Transformers.

## Installation

1. Klone das Repository
2. Installiere die Abhängigkeiten:
```bash
pip install -r requirements.txt
```

## Verwendung

Führe das Hauptprogramm aus:
```bash
python main.py
```

## Features

- Einfache Integration mit Hugging Face Transformers
- Instruction-basiertes Format
- Konfigurierbare Generierungsparameter
- GPU-Unterstützung (wenn verfügbar)

## Struktur

- `main.py`: Hauptimplementierung der InstructLLM-Klasse
- `requirements.txt`: Projektabhängigkeiten

## Anpassung

Sie können das Modell anpassen, indem Sie in der `InstructLLM`-Klasse ein anderes Basismodell auswählen:

```python
llm = InstructLLM(model_name="gpt2-medium")  # oder ein anderes Modell
