#include <iostream>
#include <stdint.h>
#include <fstream>
#include <vector>

const int ORG_RIVAL_SIZE = 0x578;
const int RIVAL_COUNT = 713;
const int TEAM_COUNT = 129;


typedef struct {
    char unchanged_block1[0x214];
    char nickname[0x1A];            // @0x214
    char unchanged_block2[0x52];
    char name[0x1A];                // @0x280
    char occupation[0x22];          // @0x29A
    char motto[0x22];               // @0x2BC
    char profile_bio_1[0x42];       // @0x2DE
    char profile_bio_2[0x42];       // @0x320
    char profile_bio_3[0x42];       // @0x362  
    char profile_bio_4[0x42];       // @0x3A4
    char profile_bio_5[0x42];       // @0x3E6
    char dialog1[0x30];
    char dialog2[0x30];
    char dialog3[0x30];
    char dialog4[0x30];
    char dialog5[0x30];
    char dialog6[0x30];
    char dialogShort1[0x18];
    char dialogShort2[0x18];
} OrgRival; //total size 0x578

void resize_rival_file(char* filename) {
    std::ifstream file(filename, std::ios::binary);
    if (!file.is_open()) {
        std::cout << "Error opening file" << std::endl;
        return;
    }
    OrgRival* rivals = new OrgRival[RIVAL_COUNT];
    const char* team_names[TEAM_COUNT][0x22];
    char footer_data[738];

    file.read((char*)rivals, ORG_RIVAL_SIZE * RIVAL_COUNT);
    file.read((char*)team_names, 0x22 * TEAM_COUNT);
    file.read(footer_data, 738);
    file.close();
}

int main(int argc, char const *argv[])
{
    if (argc < 2) {
        std::cout << "Usage: " << argv[0] << " <filename>" << std::endl;
        return 1;
    }
    resize_rival_file((char*)argv[1]);
    return 0;
}
