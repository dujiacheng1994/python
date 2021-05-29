#include <stdio.h>
#include <malloc.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct Node
{
    int data;
    struct Node * pNext;
}NODE, * PNODE;

typedef struct Stack
{
    PNODE pTop;
    PNODE pBottom;
}STACK, * PSTACK;     //PSTACK�ȼ���struct STACK *

void init(PSTACK); //��ʼ��ջ
void push(PSTACK, int );  //ѹջ
void traverse(PSTACK);    //����
bool pop(PSTACK pS,int * pVal);   //��ջ
void clear(PSTACK pS);    //���ջ

int main(void)
{
    STACK S;  //STACK�ȼ���struct Stack
    int val;
    init(&S);  //�����ջ

    push(&S, 1);  //ѹջ
    push(&S, 2);
    push(&S, 3);
    push(&S, 4);
    push(&S, 5);
    push(&S, 6);

    traverse(&S); //�������
/*
    if(pop(&S,&val))
    {
        printf("��ջ�ɹ�����ջ��Ԫ����%d\n", val);
    }
    else
    {
        printf("��ջʧ�ܣ�\n");
    }
*/
    clear(&S);
    traverse(&S);

    return 0;
}

void init(PSTACK pS)
{
    pS->pTop = (PNODE)malloc(sizeof(NODE));
    if(NULL == pS->pTop)
    {
        printf("��̬�ڴ����ʧ��\n");
        exit(-1);
    }
    else
    {
        pS->pBottom = pS->pTop;
        pS->pTop->pNext = NULL;
    }
}

void push(PSTACK pS, int val)
{
    PNODE pNew = (PNODE)malloc(sizeof(NODE));  //�����µĽڵ�
    pNew->data = val;  //��val��ֵ�����½ڵ��������
    pNew->pNext = pS->pTop; //���½ڵ��ָ����ָ����һ���ڵ�.pS->Top���ܸ�д��pS->Bottom
    pS->pTop = pNew; //pTopָ���½ڵ�
    return;
}

void traverse(PSTACK pS)
{
    PNODE p = pS->pTop;
    while(p != pS->pBottom)
    {
        printf("%d ", p->data);
        p = p->pNext;
    }
    printf("\n");
    return;
}

bool empty(PSTACK pS)
{
    if(pS->pTop == pS->pBottom)
    {
        return true;
    }
    else
    {
        return false;
    }
}

bool pop(PSTACK pS,int * pVal)
{
    if(empty(pS))
    {
        return false;
    }
    else
    {
        PNODE r = pS->pTop;
        *pVal = r->data;
        pS->pTop = r->pNext;
        free(r);
        r = NULL;
        return true;
    }
}

//���ջ
void clear(PSTACK pS)
{
    if(empty(pS))        //���
    {
        return;
    }
    else
    {
        PNODE p = pS->pTop;  //����Ԫ��pָ��ջ��Ԫ��
        PNODE q = NULL;     //����Ԫ��q����ʼֵΪ��

        while(p !=pS->pBottom)    //���ջ��Ϊ��
        {
            q = p->pNext;        //qָ��p����һ��Ԫ��
            free(p);            //�ͷ�p��ָ���ջ��Ԫ��
            p = q;               //��q��ָ���Ԫ�ظ���p
        }
        pS->pTop = pS->pBottom;
    }
}
