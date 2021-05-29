#include<math.h>
#include<stdio.h>
#include <stdlib.h>
void swapToMinusDiff(int a[],int b[],int n){
    int *temp;
    int i,j;
    int sumA=sum(a,n);
    int sumB=sum(b,n);
    if(sumA==sumB) return;
    if(sumA<sumB){
        temp=a;
        a=b;
        b=temp;
    }
    int curDiff=1;
    int oldDiff=0x7fffffff;
    int pA=-1;
    int pB=-1;
    int shift=1;
    int len=n;
    while(shift&&curDiff>0){
        shift=0;
        curDiff=sum(a,n)-sum(b,n);
        for(i=0;i<len;i++){
            for(j=0;j<len;j++){
                int temp=a[i]-b[j];
                int newDiff=abs(curDiff-2*temp);
                if(newDiff<curDiff&&newDiff<oldDiff){
                    shift=1;
                    oldDiff=newDiff;
                    pA=i;
                    pB=j;
                }
            }
        }
        if(shift){
            int temp=a[pA];
            a[pA]=b[pB];
            b[pB]=temp;
        }
    }
}
int sum(int a[],int n){
    int sum=0,i;
    for(i=0;i<n;i++){
        sum+=a[i];
    }
    return sum;
}
int main() {
    int n=6,i;
    int a[6] = {100,99,98,1,2,3};
    int b[6] = {1, 2, 3, 4,5,40};  //初始化数组

    swapToMinusDiff(a, b, 6);
    for(i=0;i<n;i++){
        printf("%d ",a[i]);
    }
    printf("\n");
    for(i=0;i<n;i++){
        printf("%d ",b[i]);
    }
    return 0;
}

