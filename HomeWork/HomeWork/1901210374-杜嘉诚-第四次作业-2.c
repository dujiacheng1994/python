#include<stdio.h>
#include<string.h>
//如果一个棋子反转了两次，那么就相当于没有反转，所以每个棋子最多反转一次才可求最小反转数
int h,w,map[30][30],temp[30][30],m[30][30];
//map数组记录棋子的初始情况，temp数组记录每个点的反转数，m数组记录最小反转数时的每个点的反转数；
int next[5][2]={{0,0},{0,1},{0,-1},{1,0},{-1,0}};
//判断此点是否是黑棋,此点的黑与白有上下左右四个和其自己本身反转次数有关；
int judge(int x,int y){
	int c=map[x][y];
	int k;
	for(k=0;k<5;k++){
		int tx=x+next[k][0];
		int ty=y+next[k][1];
		if(tx>=0&&tx<h&&ty>=0&&ty<w)
		c+=temp[tx][ty];
	}
	return c%2;
}

int dfs(){
	//从第二行开始，根据上一行的状态做出相应反转
	int i,j;
	for(i=1;i<h;i++){
		for(j=0;j<w;j++){
			if(judge(i-1,j)){
				temp[i][j]=1;//如果此点上一行对应的点是黑棋，则此点反转一次
			}
		}
	}
	for(j=0;j<w;j++){
		if(judge(h-1,j))//如果最后一行还有黑棋，返回-1；
		return -1;
	}
	int count=0;
	//计算总的反转数;
	for(i=0;i<h;i++){
		for(j=0;j<w;j++)
		count+=temp[i][j];
	}
	return count;
}

int main(){
    int i,j;
	//scanf("%d %d",&h,&w);
	int d;
	scanf("%d",&d);
	w=h=d;
	for(i=0;i<h;i++){
		for(j=0;j<w;j++)
		scanf("%1d",&map[i][j]);  //为了做到读取1101而非1 1 0 1
	}
	int min=-1;
	//从第一行开始遍历，第一行棋子的反转情况为2的W次方，用二进制状态压缩；
	for(i=0;i<(1<<w);i++){  //1<<w为2的w次方
	    memset(temp,0,sizeof(temp));
		for(j=0;j<w;j++){
			temp[0][j]=(i>>j)&1;//在此i值下第一行的反转情况
		}
		int num=dfs();//num记录当下方案的总反转数
		if(num>0&&(min<0||min>num)){
			min=num;
			memcpy(m,temp,sizeof(temp));//用memcpy函数将temp数组赋给m数组；
		}
		}
		if(min==-1){
			printf("IMPOSSIBLE\n");
		}
		else{
			printf("%d\n",min);
			//for(i=0;i<h;i++){
			//	for(j=0;j<w-1;j++)
			//	printf("%d ",m[i][j]);
			//	printf("%d\n",m[i][w-1]);
			//}
		}
	return 0;
}
