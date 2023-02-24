#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Ask user for height input
    int height = 0;
    do
    {
        height = get_int("Height: ");
    }
    // Check height between 1-8
    while (height < 1 || height > 8);

    // Rows for pyramid
    for (int i = 1; i <= height; i++)
    {
        // Spaces before hashes
        for (int k = (height - i); k > 0; k--)
        {
            printf(" ");
        }
        // Column width for pyramid
        for (int j = 0; j < i ; j++)
        {

            printf("#");
        }
        printf("\n");
    }
}
