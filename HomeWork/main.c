#include <stdio.h>
#include <stdlib.h>
#define INT_MAX 2147483647
#define INT_MIN (-INT_MAX - 1)
//ֱ�Ӷ���-2147483648�����ᱻ��ִ���Ϊ-������볣��2147483648��32λϵͳ��ʹ��unsigned int
int max(int a,int b){
    return a>=b?a:b;
}
int profit(int stock[],int n) {
    int i;
    int buy1=INT_MIN;
    int sell1=0;
    int buy2=INT_MIN;
    int sell2=0;
    if(n<=1)    //�߽�����
        return 0;
    for(i=0;i<n;i++){  //��һ����Ҫ������ʽ���
        buy1=max(buy1,-stock[i]);        //��һ�ʹ���Ľ���(����i��֮ǰ��i�۵������)
        sell1=max(sell1,buy1+stock[i]);  //����i�Ľ��� (������buy1����i)
        buy2=max(buy2,sell1-stock[i]);   //�ڶ��ʹ���Ľ���(����1����׬��)
        sell2=max(sell2,buy2+stock[i]);  //���еڶ��ʽ��׺�
    }
    return sell2;
}
int main()
{
    int n=5;  //��֪���鳤��
    int stock[5]={1,2,3,4,5};    //��֪����ֵ
    printf("%d",profit(stock,n));
    return 0;

}
