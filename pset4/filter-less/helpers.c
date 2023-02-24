#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float average = ((image[i][j].rgbtBlue + image[i][j].rgbtRed + image[i][j].rgbtGreen) / 3.0);
            double r_average = (int)round(average);
            image[i][j].rgbtBlue = r_average;
            image[i][j].rgbtRed = r_average;
            image[i][j].rgbtGreen = r_average;

        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //Convert red to sepia
            float sepia_red = (image[i][j].rgbtRed * 0.393) + (image[i][j].rgbtGreen * 0.769) + (image[i][j].rgbtBlue * 0.189);
            double r_sepia_red = (int)round(sepia_red);
            if (r_sepia_red > 255)
            {
                r_sepia_red = 255;
            }

            //Convert green to sepia
            float sepia_green = (image[i][j].rgbtRed * 0.349) + (image[i][j].rgbtGreen * 0.686) + (image[i][j].rgbtBlue * 0.168);
            double r_sepia_green = (int)round(sepia_green);
            if (r_sepia_green > 255)
            {
                r_sepia_green = 255;
            }

            //Convert blue to sepia
            float sepia_blue = (image[i][j].rgbtRed * 0.272) + (image[i][j].rgbtGreen * 0.534) + (image[i][j].rgbtBlue * 0.131);
            double r_sepia_blue = (int)round(sepia_blue);
            if (r_sepia_blue > 255)
            {
                r_sepia_blue = 255;
            }
            image[i][j].rgbtRed = r_sepia_red;
            image[i][j].rgbtBlue = r_sepia_blue;
            image[i][j].rgbtGreen = r_sepia_green;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE tmp = image[i][j];
            image[i][j] = image[i][(width - 1) - j];
            image[i][(width - 1) - j] = tmp;
        }
    }
}
// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //Make copy of image
    RGBTRIPLE tmp[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float red_count, blue_count, green_count;
            red_count = blue_count = green_count = 0;
            float pixel_counter = 0.00;

            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    int x_val = i + x;
                    int y_val = j + y;
                    // if offscreen, pass
                    if (x_val < 0 || x_val > (height - 1) || y_val < 0 || y_val > (width - 1))
                    {
                        continue;
                    }

                    red_count += image[x_val][y_val].rgbtRed;
                    blue_count += image[x_val][y_val].rgbtBlue;
                    green_count += image[x_val][y_val].rgbtGreen;

                    pixel_counter++;
                }
                //Get pixel value from average of box of pixels
                tmp[i][j].rgbtRed = round(red_count / pixel_counter);
                tmp[i][j].rgbtBlue = round(blue_count / pixel_counter);
                tmp[i][j].rgbtGreen = round(green_count / pixel_counter);
            }
        }
    }
    // Copy to actual image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = tmp[i][j].rgbtRed;
            image[i][j].rgbtBlue = tmp[i][j].rgbtBlue;
            image[i][j].rgbtGreen = tmp[i][j].rgbtGreen;
        }
    }
}
