#include <stdio.h>

int main(void)
{
    const int BYTES_TO_READ = 8;
    char buf[BYTES_TO_READ];
    FILE *fp;

    fp = fopen("grandom", "r");

    if (fp != NULL)
    {
        fseek(fp, 0, SEEK_SET);
        fread(buf, 1, BYTES_TO_READ, fp);
        printf("%s\n", buf);
    }
}