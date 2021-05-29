#include<stdio.h>
#include<malloc.h>
//����ѭ������ı�ʾ��ʵ�֣��������ͷ���head��
typedef int ElemType;
typedef struct node{
	ElemType data;
	struct node * next;
}slink;

//��������
slink *creasclink(int n){
	slink *head,*p,*s;
	int i;
	p=head=(slink*)malloc(sizeof(slink));
	for(i=1;i<=n;i++){
		s=(slink*)malloc(sizeof(slink));
		scanf("%d",&s->data);
		p->next = s;
		p=s;
	}
	p->next=head;
	return head;
}
//��������
slink *showsclink(slink *head){
	slink *p;
	p=head->next;
	while(p!=head){
		printf("%d ",p->data);
		p=p->next;
	}
	return head;
}
//�������
int getlen(slink *head){
	slink *p;
	int i=0;
	p=head->next;
	while(p!=head){
		i++;
		p=p->next;
	}
	return i;
}
//ȡԪ�ز���,ȡ��i������Ԫ�ص�ֵ
int getElem(slink *head,int i){
	int j;
	slink *p;
	p=head->next;j=1;
	if(i<1)return 0;
	while(p!=head&&j<i){
		p=p->next;
		j=j+1;
	}
	if(p==head)return 0;
	return p->data;
}
//��λ������ȡ�����е�һ��ֵΪx ��λ��
int locate(slink *head,ElemType x){
	int i;
	slink *p;
	p=head->next;i=1;
	while(p!=head&&p->data!=x){
		p=p->next;
		i++;
	}
	if(p==head)return 0;
	else return i;
}

//ɾ��������ɾ���������еĵ�i�����
int deletei(slink *head,int i){
	slink *p,*s;
	int j;
	p=head->next;j=1;
	if(i<1)return 0;
	while(p!=head&&j<i-1){
		p=p->next;
		j++;
	}
	if(p==head||p->next==head)return 0;//i���ڱ�
	s=p->next;
	p->next=s->next;
	free(s);
	return 1;
}
//����������������е�i�����֮ǰ����һ��ֵΪx�Ľ�㣩
int inserti(slink *head,ElemType x,int i){
	slink *p,*s;
	int j;
	p=head->next;j=1;
	s=(slink *)malloc(sizeof(slink));
	if(i<1)return 0;//��㲻�Ϸ�
	while(p!=head&&j<i-1){
		p=p->next;
		j++;
	}
	if(p==head||p->next==head)return 0;
	s->data=x;
	s->next=p->next;
	p->next=s;
	return 1;
}
int main(){
	slink *head;
	int i;
	head=creasclink(4);
	showsclink(head);
	printf("�������Ϊ��%d",getlen(head));

    scanf("%d",&i);
    printf("��λ��Ԫ��Ϊ��%d",locate(head,i));

    deletei(head,3);
	inserti(head,9,3);
}
