#include<stdio.h>
#define M 20//边数
#define N 10//顶点数
#define MAX 10000
void Dijkstra(int v, int dist[][N],int D[N],int p[N],int s[N]) ;
int flag[N]= {0};
int flag1=0;
int flag2=0;
typedef struct
{
    int startvex;
    int endvex;
    int length;
} edge; //边的结构体
edge T[M];
void main()
{
    /*
    状态规定：
    <1111>表示左岸人，狗，猫，兔子均在。
    0:<1111>,1:<1110>,2:<1101>,3:<1011>,4:<1010>,5:<0101>,6:<0100>,7:<0010>,8:<0001>,9:<0000>
    */
    int dist[N][N]= {{0,MAX,MAX,MAX,MAX,1,MAX,MAX,MAX,MAX}, //图的邻接矩阵，规定了两岸动物状态之间的转移关系，其中结点0表示<0,0,0,0>,结点9表示<1,1,1,1>
        {MAX,0,MAX,MAX,MAX,MAX,1,1,MAX,MAX},
        {MAX,MAX,0,MAX,MAX,1,1,MAX,1,MAX},
        {MAX,MAX,MAX,0,MAX,MAX,MAX,1,1,MAX},
        {MAX,MAX,MAX,MAX,0,MAX,MAX,1,MAX,1},
        {1,MAX,1,MAX,MAX,0,MAX,MAX,MAX,MAX},
        {MAX,1,1,MAX,MAX,MAX,0,MAX,MAX,MAX},
        {MAX,1,MAX,1,1,MAX,MAX,0,MAX,MAX},
        {MAX,MAX,1,1,MAX,MAX,MAX,MAX,0,MAX},
        {MAX,MAX,MAX,MAX,1,MAX,MAX,MAX,MAX,0}
    };
    int D[N]= {0};
    int p[N]= {0};
    int s[N]= {0};
    int num=0;
    Dijkstra(0,dist,D, p,s) ;//0表示从状态(1111)開始
}
void Dijkstra(int v, int dist[][N],int D[N],int p[N],int s[N])
{
    int i, j, k, v1, min, max=10000, pre;     /* Max中的值用以表示dist矩阵中的值*/
    v1=v;
    for( i=0; i<N; i++)              /* 各数组进行初始化*/
    {
        D[i]=dist[v1][i];
        if( D[i] != MAX )  p[i]= v1+1;
        else p[i]=0;
        s[i]=0;
    }
    s[v1]=1;
    for( i=0; i<N-1; i++)      /* 求源点到其余顶点的最短距离*/
    {
        min=10001;
        for( j=0; j<N-1; j++)
            if ( ( !s[j] )&&(D[j]<min) )          /* 找出到源点具有最短距离的边*/
            {
                min=D[j];
                k=j;
            }
        s[k]=1;  /* 将找到的顶点k送入U */
        for(j=0; j<N; j++)
            if ( (!s[j])&&(D[j]>D[k]+dist[k][j]) ) /* 调整V－U中各顶点的距离值*/
            {
                D[j]=D[k]+dist[k][j];
                p[j]=k+1;                      /* k是j的前趋*/
            }
    }                               /*  全部顶点已扩充到U中*/
    for( i=0; i<N; i++)
    {
        printf(" %d : %d ", D[i], i);
        pre=p[i];
        while ((pre!=0)&&(pre!=v+1))
        {
            printf ("<- %d ", pre-1);
            pre=p[pre-1];
        }
        printf("<-%d \n", v);
    }
    printf("结果得过河方法为：人带猫去,人回来,人带兔子去,人带猫回来,人带狗去,人回来,人带猫去");
}
