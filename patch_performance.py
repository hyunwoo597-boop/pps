#!/usr/bin/env python3
from pathlib import Path

repo = Path("core")
if not repo.exists():
    raise SystemExit("ERROR: core/ repository was not cloned.")

candidates = [
    repo / "Data" / "Sys" / "GameSettings" / "GZL.ini",
    repo / "Binary" / "Sys" / "GameSettings" / "GZL.ini",
]
target = next((p for p in candidates if p.exists()), candidates[0])
target.parent.mkdir(parents=True, exist_ok=True)
existing = target.read_text(encoding="utf-8", errors="replace") if target.exists() else ""

marker = "# BEGIN TICO_WW_PERF"
if marker not in existing:
    block = "\n".join([
        "# BEGIN TICO_WW_PERF",
        "# Nintendo Switch / Tico performance preset for The Legend of Zelda: The Wind Waker.",
        "[Core]",
        "CPUThread = True",
        "DSPHLE = True",
        "SyncGPU = False",
        "PrecisionFrameTiming = False",
        "OverclockEnable = True",
        "Overclock = 0.85",
        "",
        "[Video_Settings]",
        "InternalResolution = 1",
        "MSAA = 1",
        "SSAA = False",
        "FastDepthCalc = True",
        "EnablePixelLighting = False",
        "HiresTextures = False",
        "CacheHiresTextures = False",
        "BackendMultithreading = True",
        "",
        "[Video_Enhancements]",
        "MaxAnisotropy = 0",
        "ArbitraryMipmapDetection = True",
        "",
        "[Video_Hacks]",
        "EFBAccessEnable = True",
        "EFBToTextureEnable = False",
        "VISkip = False",
        "DeferEFBCopies = True",
        "SkipDuplicateXFBs = True",
        "BBoxEnable = False",
        "EFBEmulateFormatChanges = False",
        "# END TICO_WW_PERF",
        "",
    ])
    target.write_text(existing.rstrip() + "\n\n" + block, encoding="utf-8")
    print("Patched GameSettings:", target)
else:
    print("Performance profile already present:", target)

build = repo / "build_dolphin_standalone_nro.sh"
if not build.exists():
    raise SystemExit("ERROR: expected official build_dolphin_standalone_nro.sh not found.")

(repo / "tico_ww_perf_build.txt").write_text(
    "Tico Dolphin Wind Waker Performance Build\n"
    "CPU target: Cortex-A57\n"
    "No unsafe hardware overclock patch included.\n",
    encoding="utf-8",
)
print("Patch complete.")
