#include<iostream>
#include<queue>
#include<cstring>
#include<cstdio>
using namespace std;

const int maxn=100001;

bool vis[maxn];//�������
int step[maxn];//��¼����ÿһλ�����ߵĲ���
queue <int> q;//�������

int bfs(int n,int k)
{
    int head,next;
    q.push(n);   //��ʼFJ��nλ�ã�n���
    step[n]=0;
    vis[n]=true; //����ѷ���
    while(!q.empty())  //�����зǿ�
    {
        head=q.front();  //ȡ����
        q.pop();         //��������
        for(int i=0;i<3;i++)     //FJ�������߷�
        {
            if(i==0) next=head-1;
            else if(i==1) next=head+1;
            else next=head*2;
            if(next<0 || next>=maxn) continue; //�ų��������
            if(!vis[next])  //���nextλ��δ������
            {
                q.push(next);    //���
                step[next]=step[head]+1;  //����+1
                vis[next]=true;  //����ѷ���
            }
            if(next==k) return step[next];  //����������������ز���
        }
    }
}
int main()
{
    int n,k;
    while(cin>>n>>k)
    {
        memset(step,0,sizeof(step));
        memset(vis,false,sizeof(vis));

        while(!q.empty()) q.pop(); //ע�����ǰҪ�����
        if(n>=k) printf("%d\n",n-k);
        else printf("%d\n",bfs(n,k));
    }
    return 0;
}
