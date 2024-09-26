#include <iostream>
#include <stdint.h>
#include <stdio.h>
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

typedef struct{
    char unchanged_block1[0x214];   // @0x0
    char nickname[0x44];            // @0x214
    char unchanged_block2[0x52];    // @0x258
    char name[0x1A];                // @0x2AA
    char occupation[0x80];          // @0x2C4
    char motto[0x80];               // @0x344
    char profile_bio_1[0x94];       // @0x3C4
    char profile_bio_2[0x94];       // @0x458
    char profile_bio_3[0x94];       // @0x4EC
    char profile_bio_4[0x94];       // @0x580
    char profile_bio_5[0x94];       // @0x614
    char dialog1[0x6A];             // @0x6A8
    char dialog2[0x6A];             // @0x712
    char dialog3[0x6A];             // @0x77C
    char dialog4[0x6A];             // @0x7E6
    char dialog5[0x6A];             // @0x850
    char dialog6[0x6A];             // @0x8BA
    char dialogShort1[0x45];        // @0x924
    char dialogShort2[0x45];        // @0x969
} NewRival; //total size 0x9AE

void resize_rival_file(char* filename) {
    FILE* file = fopen(filename, "rb");
    if (!file) {
        std::cout << "Error opening file" << std::endl;
        return;
    }
    OrgRival* rivals = new OrgRival[RIVAL_COUNT];
    NewRival* new_rivals = (NewRival*)calloc(RIVAL_COUNT, sizeof(NewRival));
    std::vector<char*> team_names(TEAM_COUNT);
    char footer_data[738];

    fread(rivals, ORG_RIVAL_SIZE, RIVAL_COUNT, file);
    for (int i = 0; i < TEAM_COUNT; i++) {
        team_names[i] = new char[0x22];
        fread((char*)team_names[i], 0x22, 1, file);
    }
    fread(footer_data, 738, 1, file);
    fclose(file);

    FILE* new_file = fopen("new_rivals.bin", "wb");

    for (int i = 0; i < RIVAL_COUNT; i++) {
        memcpy(new_rivals[i].unchanged_block1, rivals[i].unchanged_block1, 0x214);
        memcpy(new_rivals[i].nickname, rivals[i].nickname, 0x1A);
        memcpy(new_rivals[i].unchanged_block2, rivals[i].unchanged_block2, 0x52);
        memcpy(new_rivals[i].name, rivals[i].name, 0x1A);
        memcpy(new_rivals[i].occupation, rivals[i].occupation, 0x22);
        memcpy(new_rivals[i].motto, rivals[i].motto, 0x22);
        memcpy(new_rivals[i].profile_bio_1, rivals[i].profile_bio_1, 0x42);
        memcpy(new_rivals[i].profile_bio_2, rivals[i].profile_bio_2, 0x42);
        memcpy(new_rivals[i].profile_bio_3, rivals[i].profile_bio_3, 0x42);
        memcpy(new_rivals[i].profile_bio_4, rivals[i].profile_bio_4, 0x42);
        memcpy(new_rivals[i].profile_bio_5, rivals[i].profile_bio_5, 0x42);
        memcpy(new_rivals[i].dialog1, rivals[i].dialog1, 0x30);
        memcpy(new_rivals[i].dialog2, rivals[i].dialog2, 0x30);
        memcpy(new_rivals[i].dialog3, rivals[i].dialog3, 0x30);
        memcpy(new_rivals[i].dialog4, rivals[i].dialog4, 0x30);
        memcpy(new_rivals[i].dialog5, rivals[i].dialog5, 0x30);
        memcpy(new_rivals[i].dialog6, rivals[i].dialog6, 0x30);
        memcpy(new_rivals[i].dialogShort1, rivals[i].dialogShort1, 0x18);
        memcpy(new_rivals[i].dialogShort2, rivals[i].dialogShort2, 0x18);
    }
    fwrite(new_rivals, sizeof(NewRival), RIVAL_COUNT, new_file);
    for (int i = 0; i < TEAM_COUNT; i++) {
        fwrite((char*)team_names[i], 0x22, 1, new_file);
    }
    fwrite(footer_data, 738, 1, new_file);
    fclose(new_file);
    delete[] rivals;
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
