//B.A.D. struct
//confusing, still incorrect in some places

struct BAD_0{    
    char name[0x1a];
    };
struct BAD_1{    
    char name[0x1c];
    };
struct BAD_2{
    char name[0x0e];
    };

struct BAD{
    u16 spacing;
    u16 value;
    BAD_2 name0;
    BAD_2 name1;
};

    
struct BADBlock{
    u32 bad_value;
    BAD bad[5];
    };

struct BADFile{
    BADBlock blocks[30];
    BAD_0 names_0[71];
    BAD_1 names_1[39];
    BAD_0 names_2[1];
    BAD_2 names_3[2];
    };

BADFile file @ 0x0;