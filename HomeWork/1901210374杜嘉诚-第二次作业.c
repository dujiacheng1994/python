#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int compare(const void *a, const void *b)
{
    char m[20];
    itoa(*(int *)a,m,10);
    char n[20];
    itoa(*(int *)b,n,10);
    strcat(m,n);
    strcat(n,m);
    return strcmp(m,n);
}
void PrintMinNumber(int numbers[],int n)
{
    qsort(numbers,n,sizeof(numbers[0]),compare);
}
int main()
{
    int st[100]={453,8,462,82,71};
    int n=5;
    int i;
    PrintMinNumber(st,n);  //传入数组与数组大小
    for(i=0;i<n;i++){
        printf("%d",st[i]);
    }
    return 0;
}
