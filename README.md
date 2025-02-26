# RBC1GP-Translation-Pipeline
### The process of translation is described in the [repository's Wiki](https://github.com/igorciz777/RBC1GP-Translation-Pipeline/wiki)
### Any translations released by me are at [Releases](https://github.com/igorciz777/RBC1GP-Translation-Pipeline/releases)

## Installation:

You need an unmodified iso dump of RACING BATTLE -C1 GRAND PRIX- [SLPM-65897]

MD5:	`8131f1e1d205de32326d7c038f8f70a3`

SHA-1:	`a00f956b669684c8dbced0bf0f19673b005aaa2f`

You also need a xdelta patcher,
personally I use DeltaPatcher or xdelta3

### Patching the game

Using a xdelta patcher, apply the main patch file `RBC1GP_English_Patch_v8.xdelta` to your iso. (remember to backup the iso, some patchers just overwrite the file without a backup)


### Widescreen patch

For emulation, the widescreen patch should be included with newest releases of PCSX2, but
if you're missing it you can move the pnach file from
the `widescreen patch` folder to `<Your PCSX2 directory>/patches/`

For hardware, use `widescreen_for_hardware_patch.xdelta` to patch your modified ISO file (one that's already patched with the main translation file)

---
Video Tutorial:

[![Video Tutorial](https://img.youtube.com/vi/RM-U211Co2Q/0.jpg)](https://www.youtube.com/watch?v=RM-U211Co2Q)

---
## Translation status

| File | Translated |
| ---- | ----------- |
| `210.bin` | $\color{green}{\textsf{100}}$% |
| `211.bin` | $\color{green}{\textsf{100}}$% |
| `212.bin` | $\color{green}{\textsf{100}}$% |
| `224.bin` | $\color{green}{\textsf{100}}$% |
| `227.bin` | $\color{green}{\textsf{100}}$% |
| `228.bin` | $\color{green}{\textsf{100}}$% |
| `229.bin` | $\color{green}{\textsf{100}}$% |
| `230.bin` | $\color{green}{\textsf{100}}$% |
| `231.bin` | $\color{green}{\textsf{100}}$% |
| `737.bin` | $\color{green}{\textsf{100}}$% |
| `Textures` | $\color{green}{\textsf{100}}$% |
| `Cutscenes` | $\color{green}{\textsf{100}}$% |
| `Executable` | $\color{green}{\textsf{100}}$% |
---	
	
### Tools that made this possible
- [GUTArchiveTools](https://github.com/igorciz777/GUTArchiveTools)
- [Cartographer](https://www.romhacking.net/utilities/647/)
- [Atlas](https://www.romhacking.net/utilities/224/)
- [Rainbow](https://github.com/marco-calautti/Rainbow)
- [ImHex](https://github.com/WerWolv/ImHex)
- [bgrep](https://github.com/nneonneo/bgrep)
- [PCSX2](https://github.com/PCSX2/pcsx2)
- [PSS Plex](https://www.zophar.net/utilities/ps2util/pss-plex.html)
- [ffmpeg](https://www.ffmpeg.org/)
