#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string input, int len);
int count_words(string input, int len);
int count_sentences(string input, int len);

int main(void)
{
    // Get user input sentence & get length
    string input = get_string("Text: ");
    int len = strlen(input);

    // Call functions to count; words, letters, sentences.
    int letters = count_letters(input, len);
    int words = count_words(input, len);
    int sentences = count_sentences(input, len);

    // Get index
    float index = 0.0588 * (letters / (words / 100.0)) - 0.296 * (sentences / (words / 100.0)) - 15.8;
    // Round to get grade realated to index
    int grade = (int)round(index);
    // Print cooresponding gardes
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }

}

int count_letters(string input, int len)
{
    // count letters in user input
    int total_letters = 0;
    for (int i = 0; i < len; i++)
    {
        if isalpha(input[i])
        {
            total_letters += 1;
        }
    }
    return total_letters;
}

int count_words(string input, int len)
{
    // Start on 1 to account for no white space at end of sentence
    int total_words = 1;
    // Count words by counting white space
    for (int i = 0; i < len; i++)
    {
        if isspace(input[i])
        {
            total_words += 1;
        }
    }
    return total_words;
}

int count_sentences(string input, int len)
{
    // Count sentences if they finish with . ? ! using ASCII number
    int count = 0;
    for (int i = 0; i < len; i++)
    {
        if (input[i] == 46 || input[i] == 63 || input[i] == 33)
        {
            count += 1;
        }
    }
    return count;
}
