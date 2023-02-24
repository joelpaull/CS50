#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

bool not_digit(char let);
int shift_letter(char letter, int shift);

int main(int argc, string argv[])
{
    // Ensure program only run with one command-line argument
    if (argc != 2)
    {
        printf("Usage:./caesar key\n");
        return 1;
    }
    // Make sure characters in (argv[1]) is a digit
    for (int i = 0; i < strlen(argv[1]); i++)
        if (not_digit(argv[1][i]))
        {
            printf("Usage:./caesar key\n");
            return 1;
        }
    // Convert argv[1] to a int
    int shift_int = atoi(argv[1]);
    // Ask for user phrase
    string phrase = get_string("plaintext: ");
    // shift letters
    printf("ciphertext: ");
    for (int i = 0; i < strlen(phrase); i++)
    {
        char shifted_letter_i = shift_letter(phrase[i], shift_int);
        printf("%c", shifted_letter_i);

    }
    printf("\n");
}

bool not_digit(char let)
{
    if (isdigit(let))
    {
        return false;
    }
    else
    {
        return true;
    }
}


int shift_letter(char letter, int shift)
{
    int shift_value = shift % 26;
    // Shift Caps letters
    if (letter >= 65 && letter <= 90)
    {
        if (shift_value + (letter - 65) > 25)
        {
            shift_value = shift_value - 26;
        }
        int shifted_letter = letter + shift_value;
        return shifted_letter;
    }
    //Shift lowercase letters
    else if (letter >= 97 && letter <= 122)
    {
        if (shift_value + (letter - 97) > 25)
        {
            shift_value = shift_value - 26;
        }
        int shifted_letter = letter + shift_value;
        return shifted_letter;
    }
    //return non letters
    else
    {
        return letter;
    }
}