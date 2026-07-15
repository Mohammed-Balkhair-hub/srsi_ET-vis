#!/usr/bin/env bash
# Copy rendered MP4s into docs/ for GitHub Pages + build ZIP downloads.
# Usage: ./scripts/sync_site_videos.sh [all|cnn|rnn|attention]

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_ROOT="$ROOT/exports/1080p"
TOPIC="${1:-all}"

sync_topic() {
  local id="$1"
  shift
  local src="$SRC_ROOT/$id"
  local vid="$ROOT/docs/videos/$id"
  local zip="$ROOT/docs/downloads/${id}-videos.zip"
  mkdir -p "$vid" "$ROOT/docs/downloads"

  local files=()
  local name
  for name in "$@"; do
    local f="$src/$name"
    if [[ ! -f "$f" ]]; then
      echo "ERROR: missing $f — run ./scripts/render_all.sh $id first" >&2
      exit 1
    fi
    files+=("$f")
  done

  echo "Syncing ${#files[@]} videos → docs/videos/$id/"
  cp -f "${files[@]}" "$vid/"

  echo "Building $zip"
  rm -f "$zip"
  (
    cd "$vid"
    zip -q -j "$zip" "$@"
  )
  ls -lh "$vid"/*.mp4 "$zip"
}

case "$TOPIC" in
  all)
    sync_topic cnn \
      01_WhyCNNs.mp4 \
      02_ConvolutionMath.mp4 \
      03_PaddingAndStride.mp4 \
      04_Pooling.mp4 \
      05_CNNPipeline.mp4
    sync_topic rnn \
      01_WhyRNNs.mp4 \
      02_RNNCellMath.mp4 \
      03_UnrollSequence.mp4 \
      04_RNNTasks.mp4
    sync_topic attention \
      01_WhyAttention.mp4 \
      02_QKVScores.mp4 \
      03_ContextOutput.mp4
    ;;
  cnn)
    sync_topic cnn \
      01_WhyCNNs.mp4 \
      02_ConvolutionMath.mp4 \
      03_PaddingAndStride.mp4 \
      04_Pooling.mp4 \
      05_CNNPipeline.mp4
    ;;
  rnn)
    sync_topic rnn \
      01_WhyRNNs.mp4 \
      02_RNNCellMath.mp4 \
      03_UnrollSequence.mp4 \
      04_RNNTasks.mp4
    ;;
  attention)
    sync_topic attention \
      01_WhyAttention.mp4 \
      02_QKVScores.mp4 \
      03_ContextOutput.mp4
    ;;
  *)
    echo "Unknown topic: $TOPIC (use all|cnn|rnn|attention)" >&2
    exit 1
    ;;
esac

echo "Done."
