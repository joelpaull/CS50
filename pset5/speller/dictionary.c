// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <cs50.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 100;

// Hash table
node *table[N];
int global_dict_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *input_word)
{
    // TODO
    // Get hash index
    int hash_index = hash(input_word);
    //Access list at this hash value
    node *tmp_p = NULL;
    tmp_p = table[hash_index];
    while (tmp_p != NULL)
    {
        if (strcasecmp(tmp_p -> word, input_word) == 0)
        {
            return true;
        }
        else
        {
            tmp_p = tmp_p -> next;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    //ittertae through char in string
    int c;
    unsigned int hash_value = 0;
    while ((c = *word++))
    {
        //add all value together
        hash_value = (hash_value * 31) + (toupper(c) - 'A');
    }
    hash_value = hash_value % N;
    return hash_value;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // open file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    // Scans dictionary word by word
    char word[LENGTH + 1];
    while (fscanf(file, "%s", word) != EOF)
    {
        // Allocate space for node
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            unload();
            return false;
        }
        // add word to node
        strcpy(n -> word, word);
        n -> next = NULL;

        //get hash index by calling hash function
        int hash_index = hash(word);

        //link new word to correcsponding list
        // link new variable to list start
        if (table[hash_index] == NULL)
        {
            table[hash_index] = n;
            global_dict_count++;
        }
        else
        {
            n -> next = table[hash_index];
            table[hash_index] = n;
            global_dict_count++;
        }
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return global_dict_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    node *cursor = NULL;
    node *tmp = NULL;
    for (int i = 0; i < N; i++)
    {
        cursor = table[i];
        tmp = table[i];
        while (cursor != NULL)
        {
            cursor = cursor -> next;
            free(tmp);
            tmp = cursor;
        }
    }
    return true;
}
