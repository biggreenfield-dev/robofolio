#!/bin/bash
mkdir -p /sessions/jolly-laughing-knuth/mnt/Claude-Robofolio/screenshots
ffmpeg -y -i "/sessions/jolly-laughing-knuth/mnt/uploads/Screen Recording 2026-03-25 at 13.35.58.mov" \
  -vf "fps=1/120,scale=1710:-1" -q:v 3 \
  /sessions/jolly-laughing-knuth/mnt/Claude-Robofolio/screenshots/frame_%03d.jpg 2>/dev/null
echo "Done: $(ls /sessions/jolly-laughing-knuth/mnt/Claude-Robofolio/screenshots/*.jpg 2>/dev/null | wc -l) frames"
