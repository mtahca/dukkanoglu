#!/usr/bin/env bash
# Eski WordPress sitesindeki görselleri assets/img altına indirir.
# Kullanım (proje kökünden):  bash tools/download_images.sh
set -u
cd "$(dirname "$0")/.."

ok=0; fail=0
while IFS=$'\t' read -r url local; do
  [ -z "$url" ] && continue
  mkdir -p "$(dirname "$local")"
  if [ -s "$local" ]; then ok=$((ok+1)); continue; fi
  if curl -fsSL --retry 2 -o "$local" "$url"; then
    ok=$((ok+1))
  else
    rm -f "$local"
    echo "İNDİRİLEMEDİ: $url" >&2
    fail=$((fail+1))
  fi
done < tools/images.txt

echo "Tamam: $ok, başarısız: $fail"
