#include<stdio.h>
#include<string.h>
#include<sys/types.h>
#include<unistd.h>
#include<stdlib.h>
int main()
{
    system("mkdir BlurOutput");
    for(int i=1;i<=40;i++)
        if(fork()==0)//child
        {
            char cmd[100]={0};
            sprintf(cmd,"python3.8 blur.py EditedVideo/test%d.mp4 BlurOutput/test%d.txt",i,i);
            printf("%s\n",cmd);
            system(cmd);
            exit(0);
        }
}
