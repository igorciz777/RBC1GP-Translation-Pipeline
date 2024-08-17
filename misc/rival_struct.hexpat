//imhex c1gp rival pattern

struct RivalData{
    u16 rival_id; // 0x0
    u16 unknwn1;  // 0x2
    u8 unknwn2;  // 0x4
    u24 unknwn3;  // 0x5
	u32 unknwn4;
    u8 car_value;  //0xC
    u24 unknwn5; 
    char unknwn_blk1[280];  // 0x10
	char unknwn_blk2[32];  // 0x128
    char unknwn_blk3[144];  // 0x148
    u8 sticker_id;
    char unknwn_blk4[59];  // 0x1d8
    char nickname[26];  // 0x214
    char unknwn_blk5[80];
	u16 experience;  // 0x27e
	char name[26];  // 0x280
    char occupation[34];  // 0x29a
	char motto[34];  // 0x2bc
    char profile_bio_1[66];  // 0x2de
    char profile_bio_2[66];  // 0x320
    char profile_bio_3[66];  // 0x362
    char profile_bio_4[66];  // 0x3a4
    char profile_bio_5[66];  // 0x3e6
    char dialog1[48];
    char dialog2[48];
    char dialog3[48];
    char dialog4[48];
    char dialog5[48];
    char dialog6[48];
    char dialogShort1[24];
    char dialogShort2[24];
    };
    
    struct Teams{
        char teamName[0x22];
    };
    
    struct Rivals{
        RivalData rivals[713];
        Teams teams[129];
        char unkwn_data[738];
    };
    Rivals rivals @ 0x00;