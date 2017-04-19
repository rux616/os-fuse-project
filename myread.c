#include <stdio.h>

int main(void)
{
    FILE *fp;
    char buf[8];
    fp = fopen("grandom", "r");

    if (fp != NULL)
    {
        fseek(fp, 0, SEEK_SET);
        fread(buf, 1, 8, fp);
        printf("%s", buf);
    }
}