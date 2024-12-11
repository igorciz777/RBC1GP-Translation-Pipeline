//B.A.D. struct

struct BAD_0{
    u16 value;
    char name[0x0e];
};
struct BAD_1{
    u32 value;
    char name[0x0e]; //wrong
    };
    
struct BADBlock{
    u32 bad_value;
    BAD_0 bads[10];//weird offset past 10
};

BADBlock blocks[20] @ 0x0;