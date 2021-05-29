#include <stdio.h>
#include <stdlib.h>
#define INT_MAX 2147483647
#define INT_MIN (-INT_MAX - 1)
//直接定义-2147483648常量会被拆分处理为-运算符与常量2147483648，32位系统会使用unsigned int
int max(int a,int b){
    return a>=b?a:b;
}
int profit(int stock[],int n) {
    int i;
    int buy1=INT_MIN;
    int sell1=0;
    int buy2=INT_MIN;
    int sell2=0;
    if(n<=1)    //边界条件
        return 0;
    for(i=0;i<n;i++){  //不一定非要完成两笔交易
        buy1=max(buy1,-stock[i]);        //第一笔购买的结余(假如i比之前的i价低则更新)
        sell1=max(sell1,buy1+stock[i]);  //卖出i的结余 (假如买buy1，卖i)
        buy2=max(buy2,sell1-stock[i]);   //第二笔购买的结余(若第1笔能赚则)
        sell2=max(sell2,buy2+stock[i]);  //进行第二笔交易后
    }
    return sell2;
}
int main()
{
    int n=5;  //已知数组长度
    int stock[5]={1,2,3,4,5};    //已知数组值
    printf("%d",profit(stock,n));
    return 0;

}
