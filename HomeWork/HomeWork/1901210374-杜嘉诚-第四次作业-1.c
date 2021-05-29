#include<stdio.h>
#include<stdlib.h>
#include<math.h>
typedef struct Node
{
    double l;//最左可被覆盖的坐标
    double r;//最右可被覆盖的坐标
}Node;
Node a[1010];
int i,j,k,n,m;
double d,x,y;
int ans;//结果
const double ZERO=1e-8;//控制精度


int cmp(Node a,Node b)//最左可被覆盖的坐标排序，从左到右排序
{
    if (a.l<b.l) return 1;
    return 0;
}

void Greedy()
{
    double now=a[0].r;
    int i;
    ans++;
    for (i=1;i<n;i++)
    {
        if (a[i].l>now+ZERO)//下个点的最左被覆盖的坐标大于当前最右可被覆盖坐标
        {
            ans++;
            now=a[i].r;
        }else if (a[i].r<now+ZERO)//下个点的最左被覆盖的坐标小于当前最右可被覆盖坐标
        {
            now=a[i].r;
        }

    }
}

int main()
{
    int i;
    scanf("%d %lf",&n,&d);
    if(n==0){
        printf("-1");
        return 0;
    }
    for(i=0;i<n;i++)
    {
        scanf("%lf %lf",&x,&y);
        if(y>d || -y>d){
            printf("-1");
            return 0;
        }
        //printf("%lf,%lf\n",x,y);
        double len=sqrt((double)(d*d-y*y));//勾股定理
        a[i].l=x-len;//计算最左可被覆盖的坐标
        a[i].r=x+len;//计算最右可被覆盖的坐标
    }
    qsort(a,n,sizeof(a[0]),cmp);  //如果是sort,头文件从stdlib.h改algorithm,n改为a+n,不需要sizeof(a[0])
    ans=0;
    Greedy();
    printf("%d",ans);
    return 0;
}
