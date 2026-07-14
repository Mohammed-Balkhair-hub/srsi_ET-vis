#!/usr/bin/env bash
# Copy rendered CNN MP4s into docs/ for GitHub Pages + build ZIP download.
# Usage (from repo root): ./scripts/sync_site_videos.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/exports/1080p"
VID="$ROOT/docs/videos/cnn"
ZIP_DIR="$ROOT/docs/downloads"
ZIP="$ZIP_DIR/cnn-videos.zip"

mkdir -p "$VID" "$ZIP_DIR"

shopt -s nullglob
files=("$SRC"/0*.mp4)
if ((${#files[@]} == 0)); then
  echo "No MP4s in exports/1080p/. Run ./scripts/render_all.sh first." >&2
  exit 1
fi

echo "Syncing ${#files[@]} videos → docs/videos/cnn/"
cp -f "${files[@]}" "$VID/"

echo "Building $ZIP"
rm -f "$ZIP"
(
  cd "$VID"
  zip -q -j "$ZIP" ./*.mp4
)

echo "Done."
ls -lh "$VID"/*.mp4 "$ZIP"
