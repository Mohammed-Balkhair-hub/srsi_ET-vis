#!/usr/bin/env bash
# Render Manim scenes at 1080p into exports/1080p/<topic>/
# Usage: ./scripts/render_all.sh [all|cnn|rnn|attention]

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

QUALITY="${QUALITY:-h}"
FLAG="-q${QUALITY}"
TOPIC="${1:-all}"

if [[ -x "$ROOT/.venv/bin/manim" ]]; then
  MANIM="$ROOT/.venv/bin/manim"
elif command -v manim >/dev/null 2>&1; then
  MANIM="manim"
else
  echo "manim not found. Activate .venv or: pip install -r requirements.txt" >&2
  exit 1
fi

EXPORT_ROOT="$ROOT/exports/1080p"
mkdir -p "$EXPORT_ROOT/cnn" "$EXPORT_ROOT/rnn" "$EXPORT_ROOT/attention"

case "$QUALITY" in
  l) RES_DIR="480p15" ;;
  m) RES_DIR="720p30" ;;
  h) RES_DIR="1080p60" ;;
  k) RES_DIR="2160p60" ;;
  *) RES_DIR="1080p60" ;;
esac

echo "Using: $MANIM ($FLAG → $RES_DIR) topic=$TOPIC"

declare -a CNN_JOBS=(
  "topics/cnn/theory/why_cnn.py|WhyCNNs|cnn|01_WhyCNNs.mp4"
  "topics/cnn/theory/convolution.py|ConvolutionMath|cnn|02_ConvolutionMath.mp4"
  "topics/cnn/theory/padding_stride.py|PaddingAndStride|cnn|03_PaddingAndStride.mp4"
  "topics/cnn/theory/pooling.py|Pooling|cnn|04_Pooling.mp4"
  "topics/cnn/theory/architecture.py|CNNPipeline|cnn|05_CNNPipeline.mp4"
  "topics/cnn/theory/pretrained.py|PretrainedModels|cnn|06_PretrainedModels.mp4"
)

declare -a RNN_JOBS=(
  "topics/rnn/theory/why_rnn.py|WhyRNNs|rnn|01_WhyRNNs.mp4"
  "topics/rnn/theory/cell_math.py|RNNCellMath|rnn|02_RNNCellMath.mp4"
  "topics/rnn/theory/unroll.py|UnrollSequence|rnn|03_UnrollSequence.mp4"
  "topics/rnn/theory/tasks.py|RNNTasks|rnn|04_RNNTasks.mp4"
)

declare -a ATT_JOBS=(
  "topics/attention/theory/why_attention.py|WhyAttention|attention|01_WhyAttention.mp4"
  "topics/attention/theory/qkv_scores.py|QKVScores|attention|02_QKVScores.mp4"
  "topics/attention/theory/context_output.py|ContextOutput|attention|03_ContextOutput.mp4"
)

JOBS=()
case "$TOPIC" in
  all)
    JOBS=("${CNN_JOBS[@]}" "${RNN_JOBS[@]}" "${ATT_JOBS[@]}")
    ;;
  cnn) JOBS=("${CNN_JOBS[@]}") ;;
  rnn) JOBS=("${RNN_JOBS[@]}") ;;
  attention) JOBS=("${ATT_JOBS[@]}") ;;
  *)
    echo "Unknown topic: $TOPIC (use all|cnn|rnn|attention)" >&2
    exit 1
    ;;
esac

for job in "${JOBS[@]}"; do
  IFS='|' read -r file scene topic_id export_name <<<"$job"
  module="$(basename "$file" .py)"
  echo ""
  echo "======== $scene ========"
  "$MANIM" "$FLAG" --disable_caching "$file" "$scene"
  src_mp4="$ROOT/media/videos/$module/$RES_DIR/${scene}.mp4"
  if [[ ! -f "$src_mp4" ]]; then
    echo "ERROR: missing $src_mp4" >&2
    exit 1
  fi
  dest="$EXPORT_ROOT/$topic_id/$export_name"
  mkdir -p "$(dirname "$dest")"
  cp -f "$src_mp4" "$dest"
  echo "→ exports/1080p/$topic_id/$export_name"
done

echo ""
echo "Done. Sync to the website:"
echo "  ./scripts/sync_site_videos.sh $TOPIC"
