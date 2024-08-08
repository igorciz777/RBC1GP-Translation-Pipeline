//event struct
struct Event{ //struct size 0x68
    u8 id;
    u24 smthing0;
    u32 smthing1[18];
    char eventName[28];
    };

char weirdNumbers0[0x6c0] @ 0x0;
Event events[149] @ 0x6c0;
char weirdNumbers1[0x21c] @ 0x4348;
char weirdNumbers2[0x360] @ 0x4564;