#!/usr/bin/env bash
# Render CNN Manim scenes at 1080p into exports/1080p/
# Usage (from repo root): ./scripts/render_all.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

QUALITY="${QUALITY:-h}"
FLAG="-q${QUALITY}"

if [[ -x "$ROOT/.venv/bin/manim" ]]; then
  MANIM="$ROOT/.venv/bin/manim"
elif command -v manim >/dev/null 2>&1; then
  MANIM="manim"
else
  echo "manim not found. Activate .venv or: pip install -r requirements.txt" >&2
  exit 1
fi

EXPORT_DIR="$ROOT/exports/1080p"
mkdir -p "$EXPORT_DIR"

case "$QUALITY" in
  l) RES_DIR="480p15" ;;
  m) RES_DIR="720p30" ;;
  h) RES_DIR="1080p60" ;;
  k) RES_DIR="2160p60" ;;
  *) RES_DIR="1080p60" ;;
esac

echo "Using: $MANIM ($FLAG → $RES_DIR)"

declare -a JOBS=(
  "topics/cnn/theory/why_cnn.py|WhyCNNs|01_WhyCNNs.mp4"
  "topics/cnn/theory/convolution.py|ConvolutionMath|02_ConvolutionMath.mp4"
  "topics/cnn/theory/padding_stride.py|PaddingAndStride|03_PaddingAndStride.mp4"
  "topics/cnn/theory/pooling.py|Pooling|04_Pooling.mp4"
  "topics/cnn/theory/architecture.py|CNNPipeline|05_CNNPipeline.mp4"
)

for job in "${JOBS[@]}"; do
  IFS='|' read -r file scene export_name <<<"$job"
  module="$(basename "$file" .py)"
  echo ""
  echo "======== $scene ========"
  "$MANIM" "$FLAG" --disable_caching "$file" "$scene"
  src_mp4="$ROOT/media/videos/$module/$RES_DIR/${scene}.mp4"
  if [[ ! -f "$src_mp4" ]]; then
    echo "ERROR: missing $src_mp4" >&2
    exit 1
  fi
  cp -f "$src_mp4" "$EXPORT_DIR/$export_name"
  echo "→ exports/1080p/$export_name"
done

echo ""
echo "Done. Optionally sync to the website:"
echo "  ./scripts/sync_site_videos.sh"
