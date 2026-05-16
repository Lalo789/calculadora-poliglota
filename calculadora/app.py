from flask import Flask, request, jsonify, render_template
import subprocess
import json
import os
import tempfile

app = Flask(__name__)

# ─── Comunicación con Prolog ───────────────────────────────────────────────────

def consultar_prolog(operacion, args):
    """Envía una consulta a SWI-Prolog y regresa el resultado."""
    query = ""
    if operacion == "es_primo":
        query = f"es_primo({args[0]}), write(true), halt ; write(false), halt."
    elif operacion == "es_par":
        query = f"(0 is {args[0]} mod 2 -> write(true) ; write(false)), halt."
    elif operacion == "factorial":
        query = f"factorial({args[0]}, R), write(R), halt."
    elif operacion == "mcd":
        query = f"mcd({args[0]}, {args[1]}, R), write(R), halt."

    try:
        resultado = subprocess.run(
            ["swipl", "-q", "-l", "logica.pl", "-g", query],
            capture_output=True, text=True, timeout=5
        )
        salida = resultado.stdout.strip()
        return salida if salida else "error"
    except FileNotFoundError:
        return "SWI-Prolog no instalado"
    except subprocess.TimeoutExpired:
        return "timeout"

# ─── Comunicación con Common Lisp ─────────────────────────────────────────────

def consultar_lisp(operacion, args):
    """Envía una expresión a SBCL (Common Lisp) y regresa el resultado."""
    if operacion == "suma":
        expr = f"(+ {args[0]} {args[1]})"
    elif operacion == "resta":
        expr = f"(- {args[0]} {args[1]})"
    elif operacion == "multiplicacion":
        expr = f"(* {args[0]} {args[1]})"
    elif operacion == "division":
        if float(args[1]) == 0:
            return "error: division entre cero"
        expr = f"(/ (float {args[0]}) (float {args[1]}))"
    elif operacion == "potencia":
        expr = f"(expt {args[0]} {args[1]})"
    elif operacion == "raiz":
        if float(args[0]) < 0:
            return "error: raiz de numero negativo"
        expr = f"(sqrt (float {args[0]}))"
    elif operacion == "log":
        if float(args[0]) <= 0:
            return "error: logaritmo de numero no positivo"
        expr = f"(log (float {args[0]}))"
    else:
        return "operacion desconocida"

    lisp_code = f"""
(load "calculos.lisp")
(let ((resultado {expr}))
  (format t "~a" resultado))
"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.lisp', delete=False) as f:
            f.write(lisp_code)
            tmp_path = f.name

        resultado = subprocess.run(
            ["sbcl", "--noinform", "--load", tmp_path, "--eval", "(quit)"],
            capture_output=True, text=True, timeout=5
        )
        os.unlink(tmp_path)
        salida = resultado.stdout.strip()
        return salida if salida else resultado.stderr.strip() or "error"
    except FileNotFoundError:
        # Fallback: Python hace el cálculo si Lisp no está instalado
        return calcular_python_fallback(operacion, args)
    except subprocess.TimeoutExpired:
        return "timeout"

def calcular_python_fallback(operacion, args):
    """Fallback en Python si Common Lisp no está instalado."""
    import math
    try:
        a = float(args[0])
        b = float(args[1]) if len(args) > 1 else None
        if operacion == "suma":        return str(a + b)
        if operacion == "resta":       return str(a - b)
        if operacion == "multiplicacion": return str(a * b)
        if operacion == "division":    return str(a / b) if b != 0 else "error: division entre cero"
        if operacion == "potencia":    return str(a ** b)
        if operacion == "raiz":        return str(math.sqrt(a))
        if operacion == "log":         return str(math.log(a))
    except Exception as e:
        return f"error: {e}"

# ─── Rutas ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calcular", methods=["POST"])
def calcular():
    data = request.get_json()
    operacion = data.get("operacion")
    args = data.get("args", [])

    # Operaciones matemáticas → Common Lisp
    ops_lisp = ["suma", "resta", "multiplicacion", "division", "potencia", "raiz", "log"]
    # Operaciones lógicas → Prolog
    ops_prolog = ["es_primo", "es_par", "factorial", "mcd"]

    if operacion in ops_lisp:
        resultado = consultar_lisp(operacion, args)
        motor = "Common Lisp (SBCL)"
    elif operacion in ops_prolog:
        resultado = consultar_prolog(operacion, args)
        motor = "Prolog (SWI-Prolog)"
    else:
        return jsonify({"error": "Operación desconocida"}), 400

    return jsonify({
        "operacion": operacion,
        "args": args,
        "resultado": resultado,
        "motor": motor
    })

@app.route("/estado")
def estado():
    """Verifica qué motores están disponibles."""
    prolog_ok = subprocess.run(["which", "swipl"], capture_output=True).returncode == 0
    lisp_ok   = subprocess.run(["which", "sbcl"],  capture_output=True).returncode == 0
    return jsonify({
        "python": True,
        "prolog": prolog_ok,
        "lisp": lisp_ok
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
