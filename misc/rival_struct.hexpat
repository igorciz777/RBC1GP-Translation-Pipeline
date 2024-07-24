//imhex c1gp rival pattern

struct RivalData{
    u24 idx;
    u32 something;
    u32 something2;
    u8 zero1;
    u8 weirdCarValue; //sometimes changes rims size sometimes color
    char zero2[11];
    u8 carBodyId;
    char unknown[507];
    char nickname[24];
    char unknown2[84];
    char name[26];
    char job[34];
    char bio1[232];
    char dialog1[132];
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