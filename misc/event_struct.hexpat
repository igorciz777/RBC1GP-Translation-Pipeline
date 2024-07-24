struct EventData{
    u32 ff_1;
    u32 smthing1[3];
    u32 ff_2;
    u32 smthing2;
    u32 ff_3;
    u32 smthing3[3];
    u32 ff_4;
    u32 ff_5;
    u32 smthing4[5];
    char eventName[28];
    u32 smthing5[2];
    };
    
struct EventsFile{
    EventData events[149];
    };
    
    EventsFile eventsFile @ 0x6c8;