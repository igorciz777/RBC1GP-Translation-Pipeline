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
| `231.bin` |   0% |
| `737.bin` | $\color{green}{\textsf{100}}$% |
| `Textures` |  99% |
| `Cutscenes` |   99% |
| `Executable` |  99% |
---
## Installation
Extract your copy of RACING BATTLE -C1 GRAND PRIX- into a folder.

To patch your game files you will need GUT Archive Tools (WARNING !!! v0.3.1 and up, very big changes were made to allow bigger files):
(https://github.com/igorciz777/GUTArchiveTools/releases) 

To repack the game files you will need ImgBurn
(https://www.imgburn.com/)


### Inside this archive there are two folders: 

- in:
  
	This folder contains the main translation files. These files come from BUILD.DAT and need to be reinserted using GUT Archive Tool.
		
	Use this command on your game files to patch them (modify the command according to your directiories):
	
		.\gut_archive.exe -r .\BUILD.TOC .\BUILD.DAT .\in\
		
	If you did everything correctly the commandline should output:
	
		Reading file info from TOC...
		Rebuilding GUT Archive...
		Processing file id:224
		Block size: 16384
		(.......)
		GUT Archive rebuilt successfully
	
		
		
- elf:
- 
	This folder contains two ways of patching the executable.
	
	---
	
	For PCSX2 use the .pnach file. 
	
	Simply put it inside your PCSX2\cheats\ folder
	
	After moving the file activate it in Game Properties > Cheats.
	
	---
	
	For OPL there is a pre-patched executable file `SLPM_658.97_patchedElf`.
	
	It was patched with PS2PatchElf using the .pnach file mentioned above.
	
	Rename the file to `SLPM_658.97` and with it replace the executable inside your game folder.
	
	
### Repack

	Now you need to repack the game files using ImgBurn with default ISO settings

	"Create image file from files/folders" -> Add your game folder as the source -> "Build" -> Select your save destination -> Select "Yes" on everything
	
	
	
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
