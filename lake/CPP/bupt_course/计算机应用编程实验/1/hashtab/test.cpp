#include <iostream>
#include <fcntl.h>
#include <io.h>

using namespace std;


int main(int argc, char *argv[]) {
    // open res file
    FILE *fp_res = fopen("/media/zx/6C24B6F224B6BE80/Users/zhang/Desktop/北邮/1/计算机应用编程实验/1/hashtab/test", "w+");
    if (fp_res == NULL) {
        cout << "fail to open result.txt" << endl;
        return 0;
    }

    fputs("test", fp_res);
    fputc('\n', fp_res);

    int fsz=ftell(fp_res);
    chsize(fileno(fp_res),fsz-1);

    fclose(fp_res);
}
