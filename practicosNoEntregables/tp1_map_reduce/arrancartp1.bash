#!/bin/bash

set -e

echo "======================================"
echo "   Iniciando entorno TP1 - Big Data"
echo "======================================"

# Directorio donde está este script
TP1_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "📁 Directorio del TP1:"
echo "$TP1_DIR"

# --------------------------------------------------
# 1. Verificar Python 3
# --------------------------------------------------

echo ""
echo "🐍 Verificando Python 3..."

if ! command -v python3 &> /dev/null; then
    echo "Python 3 no está instalado."
    echo "Instalando Python 3..."

    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip
else
    echo "Python encontrado:"
    python3 --version
fi

# --------------------------------------------------
# 2. Verificar venv
# --------------------------------------------------

echo ""
echo "🔧 Verificando soporte para entornos virtuales..."

if ! python3 -m venv --help &> /dev/null; then
    echo "Instalando python3-venv..."
    sudo apt update
    sudo apt install -y python3-venv
fi

# --------------------------------------------------
# 3. Crear entorno virtual si no existe
# --------------------------------------------------

if [ ! -d "$TP1_DIR/.venv" ]; then
    echo ""
    echo "📦 Creando entorno virtual..."

    python3 -m venv "$TP1_DIR/.venv"

    echo "✅ Entorno virtual creado."
else
    echo ""
    echo "✅ El entorno virtual ya existe."
fi

# --------------------------------------------------
# 4. Activar entorno virtual
# --------------------------------------------------

echo ""
echo "⚡ Activando entorno virtual..."

source "$TP1_DIR/.venv/bin/activate"

echo "Python utilizado:"
which python

echo "Versión:"
python --version

# --------------------------------------------------
# 5. Actualizar pip
# --------------------------------------------------

echo ""
echo "📥 Actualizando pip..."

python -m pip install --upgrade pip

# --------------------------------------------------
# 6. Verificar estructura del TP
# --------------------------------------------------

echo ""
echo "📂 Verificando archivos del TP..."

if [ -d "$TP1_DIR/segundaParte" ]; then
    echo "✅ segundaParte encontrada"
else
    echo "⚠️ No se encontró la carpeta segundaParte"
fi

if [ -f "$TP1_DIR/segundaParte/MRE.py" ]; then
    echo "✅ MRE.py encontrado"
else
    echo "⚠️ No se encontró MRE.py"
fi

if [ -d "$TP1_DIR/segundaParte/input" ]; then
    echo "✅ input encontrado"
else
    echo "⚠️ No se encontró la carpeta input"
fi

# --------------------------------------------------
# 7. Entrar a segundaParte
# --------------------------------------------------

echo ""
echo "📁 Entrando a segundaParte..."

cd "$TP1_DIR/segundaParte"

echo "Directorio actual:"
pwd

# --------------------------------------------------
# 8. Final
# --------------------------------------------------

echo ""
echo "======================================"
echo "       ✅ TP1 LISTO"
echo "======================================"
echo ""
echo "Python:"
python --version

echo ""
echo "Entorno:"
echo "$VIRTUAL_ENV"

echo ""
echo "Directorio:"
pwd

echo ""
echo "Para ejecutar el TP:"
echo ""
echo "    python scriptMapReduce.py"
echo ""
echo "======================================"
