#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2 )
    {
        printf("Maximum of one file can be selected");
        return 1;
    }
    int jpeg_count = 0;
    int BLOCK_SIZE = 512;

    // Open file
    FILE *file = fopen(argv[1], "r");

    //Check file correct format
    if (file == NULL)
    {
        printf("Could not open file");
        return 1;
    }

    // Create buffer of size 512
    BYTE buffer[BLOCK_SIZE];

    //Create empty output file
    FILE *output = NULL;
    char image[8];

    while(fread(buffer, 1, BLOCK_SIZE, file) == BLOCK_SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (jpeg_count == 0)
            {
                sprintf(image, "%03i.jpg", jpeg_count);

                output = fopen(image, "w");

                fwrite(buffer, 1, BLOCK_SIZE, output);

                jpeg_count++;
            }
            else if (jpeg_count > 0)
            {
                fclose(output);

                sprintf(image, "%03i.jpg", jpeg_count);

                output = fopen(image, "w");

                fwrite(buffer, 1, BLOCK_SIZE, output);

                jpeg_count++;
            }
        }
        else if (jpeg_count > 0)
        {
            fwrite(buffer, 1, BLOCK_SIZE, output);
        }

    }

    fclose(output);
    fclose(file);
}