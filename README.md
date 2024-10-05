# RBC1GP-Translation-Pipeline
### All necessary info is in the [repository's Wiki](https://github.com/igorciz777/RBC1GP-Translation-Pipeline/wiki)
### Any translations released by me are at [Releases](https://github.com/igorciz777/RBC1GP-Translation-Pipeline/releases)
---
## Translation status
(99% is pretty much 100% but with issues, possible glitches etc.)
| File | Translated |
| ---- | ----------- |
| `210.bin` |   0% |
| `211.bin` |   0% |
| `212.bin` |   0% |
| `224.bin` | $\color{green}{\textsf{100}}$% |
| `227.bin` | $\color{green}{\textsf{100}}$% |
| `228.bin` | $\color{green}{\textsf{100}}$% |
| `229.bin` | $\color{green}{\textsf{100}}$% |
| `230.bin` | $\color{green}{\textsf{100}}$% |
| `231.bin` | 67.8% |
| `737.bin` | $\color{green}{\textsf{100}}$% |
| `Textures` |  $\color{green}{\textsf{100}}$% |
| `Cutscenes` |   99% |
| `Executable` |  99% |
---
## Installation:
You need an unmodified iso dump of RACING BATTLE -C1 GRAND PRIX- [SLPM-65897]

MD5: 8131f1e1d205de32326d7c038f8f70a3

You also need a xdelta patcher,
personally I use DeltaPatcher or xdelta3

### Patching the game for emulation
Using a xdelta patcher, apply the main patch file `tl_patch_vx.xdelta` to your iso. (remember to backup the iso, some patchers just overwrite the file without a backup)
	
Move the `SLPM-65897_1C087362.pnach` file to <your PCSX2 folder>/cheats/


### Patching the game for hardware
Using a xdelta patcher, apply the main patch file `tl_patch_vx.xdelta` to your iso.

After that, apply the `hw_patch_vx.xdelta` patch to your modified iso from previous step.
	
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
