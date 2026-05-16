# ⚡ Calculadora Políglota
### Python · Common Lisp · Prolog

---

## 🏗️ Arquitectura

| Capa | Lenguaje | Rol |
|------|----------|-----|
| Frontend / API | **Python** (Flask) | Recibe datos, sirve la web, conecta los motores |
| Lógica | **Prolog** (SWI-Prolog) | Es primo, factorial, MCD, es par |
| Matemáticas | **Common Lisp** (SBCL) | Suma, resta, mult., div., potencia, raíz, log |

> Si Lisp o Prolog no están instalados, Python hace el cálculo como fallback automático.

---

## 🚀 Opción A — GitHub Codespaces (tú)

1. Sube el proyecto a GitHub.
2. Abre el repositorio → `Code` → `Codespaces` → **New codespace**.
3. Espera a que el contenedor termine (instala todo solo gracias a `.devcontainer/`).
4. En la terminal del Codespace:
   ```bash
   python app.py
   ```
5. Codespaces abrirá automáticamente el puerto 5000 en el navegador.

---

## 💻 Opción B — VS Code local (tus compañeros)

### Requisitos previos
```bash
# Ubuntu/Debian
sudo apt install swi-prolog sbcl python3-pip

# macOS (Homebrew)
brew install swi-prolog sbcl

# Windows → instalar manualmente:
# SWI-Prolog: https://www.swi-prolog.org/Download.html
# SBCL:       https://www.sbcl.org/platform-table.html
```

### Pasos
```bash
# 1. Clonar / abrir el proyecto
cd calculadora

# 2. Instalar Flask
pip install -r requirements.txt

# 3. Ejecutar
python app.py

# 4. Abrir en el navegador
# http://localhost:5000
```

---

## 📁 Estructura del proyecto

```
calculadora/
├── app.py              ← Python: servidor Flask (cerebro principal)
├── logica.pl           ← Prolog: reglas lógicas
├── calculos.lisp       ← Common Lisp: operaciones matemáticas
├── requirements.txt    ← Dependencias Python
├── templates/
│   └── index.html      ← Interfaz web
└── .devcontainer/
    ├── devcontainer.json ← Config de Codespaces
    └── setup.sh          ← Script de instalación automática
```

---

## ⚙️ Operaciones disponibles

### 🔢 Common Lisp (matemáticas)
- Suma, Resta, Multiplicación, División
- Potencia (`a^b`)
- Raíz cuadrada
- Logaritmo natural

### 🧠 Prolog (lógica)
- ¿Es primo?
- ¿Es par?
- Factorial (`n!`)
- MCD (Máximo Común Divisor)

---

## 🖥️ Para subir a servidor (tus compañeros)

El proyecto es una app Flask estándar. Se puede desplegar en:
- **Railway / Render / Fly.io** (gratis) — solo agregar `gunicorn` a requirements.txt
- **VPS propio** — `gunicorn -w 4 app:app`
- **Docker** — agregar un Dockerfile con `FROM python:3.11` + instalar swipl y sbcl
