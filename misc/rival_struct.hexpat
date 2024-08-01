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
    char unknwn_blk3[204];  // 0x148
    char nickname[106];  // 0x214
	u16 unknwn6;  // 0x27e
	char name[26];
    char occupation[34];
	char motto[34];
    char profile_bio_1[66];
    char profile_bio_2[66];
    char profile_bio_3[66];
    char dialog_1_line_1[66];
    char dialog_1_line_2[66];
    char dialog2[48];
    char dialog3[48];
    char dialog4[48];
    char dialog5[48];
    char dialog6[48];
    char dialog7[48];
    char dialogShort1[24];
    char dialogShort2[24];
    };
    
    struct Rivals{
        RivalData rivals[713];
    };
    Rivals rivals @ 0x00;