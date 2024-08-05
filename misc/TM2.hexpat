//PS2 TIM2 Texture file format

bitfield GsTex{
    TBP0:14;
    TBW:6;
    PSM:6;
    TW:4;
    TH:4;
    TCC:1;
    TFX:2;
    CBP:14;
    CPSM:4;
    CSM:1;
    CSA:5;
    CLD:3;
};

// TIM2 picture header + data
struct TIM2_PICTURE{
	u32 TotalSize; // total size of the picture data in bytes
	u32 ClutSize; // CLUT data size in bytes
	u32 ImageSize; // image data size in bytes
	u16 HeaderSize; // amount of headers
	u16 ClutColors; // colors in CLUT
	char PictFormat; // picture format
	char MipMapTextures; // number of MIPMAP texture
	char ClutType; // CLUT type
	char ImageType; // image type
	u16 ImageWidth; // width of image (not in bits)
	u16 ImageHeight; // height of image (not in bits)

	GsTex GsTex0; // TEX0
	GsTex GsTex1; // TEX1
	u32 GsTexaFbaPabe; // bitfield of TEXA, FBA and PABE
	u32 GsTexClut; // TEXCLUT (lower 32 bits)
	char pad[80];
	char pictureData[ImageSize];
	char clutData[ClutSize];
}[[hex::visualize("image", this.pictureData)]];

// TIM2 file header
struct TIM2_FILEHEADER{
	char FileId[4]; // file ID ('T','I','M','2' or 'C','L','T','2')
	char FormatVersion; // version of file format
	char FormatId; // ID of format
	u16 PictureCount; // number of picture data
	char pad[120]; // for alignment
	TIM2_PICTURE pictures[PictureCount];
};

// TIM2 MIPMAP header
struct TIM2_MIPMAPHEADER{
	u64 GsMiptbp1; // MIPTBP1 (actual 64 bit image)
	u64 GsMiptbp2; // MIPTBP2 (actual 64 bit image)
	u32 MMImageSize[0]; // image size of N-th MIPMAP texture in bytes
};


// TIM2 extended header
struct TIM2_EXHEADER{
	char ExHeaderId[4]; // extended header ID ('e','X','t','\x00')
	u32 UserSpaceSize; // size of user space
	u32 UserDataSize; // size of user data
	u32 Reserved; // reserved
};

TIM2_FILEHEADER header @ 0x00;