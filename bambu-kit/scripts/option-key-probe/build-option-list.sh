#!/usr/bin/env bash
# 슬라이서 태그 소스로 판정 프로그램을 빌드하고 옵션 목록(TSV)을 다시 만든다.
#
# usage: bash build-option-list.sh <orca|bambu> [출력 .tsv]
#   출력 기본값: skills/bambu-print-profile/references/option-keys/<슬라이서>-<버전>.tsv
#   작업 폴더:   $OPTION_KEY_PROBE_WORK (기본 ${TMPDIR:-/tmp}/bambu-kit-option-key-probe) — 받은 소스와 헤더를 재사용한다
#
# 슬라이서 전체를 빌드하지 않는다. 옵션 등록부(PrintConfig·Config)와 프리셋 기본값(Preset·PresetBundle 생성자)만
# 컴파일하고, 실행 중 부르지 않는 기호는 링크 시점에 비워 둔다 (-undefined dynamic_lookup).
# 새 슬라이서 버전에서 실행이 "symbol not found" 로 죽으면 그 기호를 정의한 소스를 SOURCES 에 더한다.
set -euo pipefail

SLICER=${1:?usage: build-option-list.sh <orca|bambu> [출력 .tsv]}
HERE=$(cd "$(dirname "$0")" && pwd)
WORK=${OPTION_KEY_PROBE_WORK:-${TMPDIR:-/tmp}/bambu-kit-option-key-probe}
THIRD="$WORK/third"

case "$SLICER" in
  orca)
    REPO=OrcaSlicer/OrcaSlicer; TAG=v2.4.2; VERSION=2.4.2
    SPARSE=(cmake deps deps_src/admesh deps_src/clipper deps_src/clipper2 deps_src/eigen deps_src/fast_float
            deps_src/miniz deps_src/nanosvg deps_src/nlohmann deps_src/semver src/cereal src/clipper src/eigen
            src/libnest2d src/libslic3r src/nlohmann src/slic3r/Utils)
    SOURCES=(PrintConfig Config libslic3r Polygon clipper Polyline MaterialType Preset AppConfig)
    C_SOURCES=(deps_src/semver/semver.c)
    VERSION_VALUES=(SLIC3R_APP_NAME=OrcaSlicer SLIC3R_APP_KEY=OrcaSlicer "SLIC3R_VERSION=$VERSION"
                    "SoftFever_VERSION=$VERSION" SLIC3R_BUILD_ID=probe BBL_INTERNAL_TESTING=0
                    ORCA_CHECK_GCODE_PLACEHOLDERS=0) ;;
  bambu)
    REPO=bambulab/BambuStudio; TAG=v02.08.02.61; VERSION=02.08.02.61
    SPARSE=(cmake deps src/boost src/cereal src/clipper src/eigen src/fast_float src/libslic3r src/miniz
            src/nlohmann src/semver)
    SOURCES=(PrintConfig Config Polygon clipper Polyline Preset AppConfig)
    C_SOURCES=(src/semver/semver.c)
    VERSION_VALUES=(SLIC3R_APP_NAME=BambuStudio SLIC3R_APP_KEY=BambuStudio "SLIC3R_VERSION=$VERSION"
                    SLIC3R_BUILD_ID=probe SLIC3R_BUILD_TIME=probe SLIC3R_COMPILE_VERSION=probe
                    BBL_RELEASE_TO_PUBLIC=1 BBL_INTERNAL_TESTING=0) ;;
  *) echo "usage: build-option-list.sh <orca|bambu> [출력 .tsv]" >&2; exit 2 ;;
esac

OUT_TSV=${2:-"$HERE/../../skills/bambu-print-profile/references/option-keys/$SLICER-$VERSION.tsv"}
SRC="$WORK/$SLICER"
BUILD="$WORK/build-$SLICER"
mkdir -p "$THIRD" "$BUILD/gen"

# 헤더만 쓰는 외부 라이브러리. 버전은 두 슬라이서의 deps/ 가 받는 것과 맞췄다
fetch() {   # fetch <확인할 경로> <URL> [tar 가 풀 경로]
  [ -e "$THIRD/$1" ] && return 0
  echo "받는 중: $2"
  curl -fsSL "$2" | tar xz -C "$THIRD" ${3:+"$3"}
}
fetch boost_1_84_0/boost https://archives.boost.io/release/1.84.0/source/boost_1_84_0.tar.gz boost_1_84_0/boost
fetch cereal-1.3.0 https://github.com/USCiLab/cereal/archive/refs/tags/v1.3.0.tar.gz
fetch eigen-5.0.1 https://gitlab.com/libeigen/eigen/-/archive/5.0.1/eigen-5.0.1.tar.gz
fetch oneTBB-2021.5.0 https://github.com/oneapi-src/oneTBB/archive/refs/tags/v2021.5.0.tar.gz

if [ ! -d "$SRC/.git" ]; then
  git -c advice.detachedHead=false clone -q --depth 1 --branch "$TAG" --filter=blob:none --sparse "https://github.com/$REPO.git" "$SRC"
fi
git -C "$SRC" sparse-checkout set "${SPARSE[@]}" >/dev/null
echo "$SLICER $TAG · $(git -C "$SRC" rev-parse --short HEAD)"

# CMake 가 만드는 버전 헤더를 같은 틀(.h.in)로 채운다
SUBST=()
for pair in "${VERSION_VALUES[@]}"; do SUBST+=(-e "s|@${pair%%=*}@|${pair#*=}|g"); done
sed "${SUBST[@]}" "$SRC/src/libslic3r/libslic3r_version.h.in" > "$BUILD/gen/libslic3r_version.h"
if grep -q '@[A-Za-z_]*@' "$BUILD/gen/libslic3r_version.h"; then
  echo "버전 헤더에 못 채운 자리가 남았다:" >&2; grep '@[A-Za-z_]*@' "$BUILD/gen/libslic3r_version.h" >&2; exit 1
fi

python3 "$HERE/extract-bundle-ctor.py" "$SRC/src/libslic3r/PresetBundle.cpp" "$BUILD/preset_bundle_ctor.cpp"

# 로그 매크로를 비운다 — BambuStudio 는 정적 초기화 중에 부트 로그를 불러 링크하지 않은 로그 라이브러리에서 죽는다
FLAGS=(-std=c++17 -O1 -DSLIC3R_GUI -DBBL_RELEASE_TO_PUBLIC=1 -DNDEBUG -DUSE_TBB -DTBB_USE_CAPTURED_EXCEPTION=0
  -I"$BUILD/gen" -I"$SRC/src" -I"$SRC/src/libslic3r" -I"$SRC/deps_src" -I"$SRC/deps_src/nlohmann"
  -I"$SRC/deps_src/clipper" -I"$SRC/deps_src/fast_float" -I"$SRC/deps_src/semver" -I"$SRC/src/nlohmann"
  -I"$SRC/src/eigen" -I"$SRC/src/clipper" -I"$THIRD/boost_1_84_0" -I"$THIRD/cereal-1.3.0/include"
  -I"$THIRD/eigen-5.0.1" -I"$THIRD/oneTBB-2021.5.0/include" -I"$HERE/stub" -include "$HERE/stub/nolog.hpp")

OBJECTS=()
compile() {   # compile <소스> <목적 파일>
  [ "$2" -nt "$1" ] || clang++ "${FLAGS[@]}" -w -c "$1" -o "$2"
  OBJECTS+=("$2")
}
for name in "${SOURCES[@]}"; do compile "$SRC/src/libslic3r/$name.cpp" "$BUILD/$name.o"; done
compile "$BUILD/preset_bundle_ctor.cpp" "$BUILD/preset_bundle_ctor.o"
for c_source in "${C_SOURCES[@]}"; do
  object="$BUILD/$(basename "$c_source" .c).c.o"
  [ "$object" -nt "$SRC/$c_source" ] || clang -O1 -w -c "$SRC/$c_source" -o "$object"
  OBJECTS+=("$object")
done
clang++ "${FLAGS[@]}" -w -c "$HERE/option_key_probe.cpp" -o "$BUILD/option_key_probe.o"
clang++ "$BUILD/option_key_probe.o" "${OBJECTS[@]}" -Wl,-undefined,dynamic_lookup -o "$BUILD/option_key_probe"

mkdir -p "$(dirname "$OUT_TSV")"
python3 "$HERE/generate-option-list.py" "$BUILD/option_key_probe" "$SRC" "$OUT_TSV"
