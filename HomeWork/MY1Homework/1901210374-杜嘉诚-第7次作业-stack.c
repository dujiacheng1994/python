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
}STACK, * PSTACK;     //PSTACK等价于struct STACK *

void init(PSTACK); //初始化栈
void push(PSTACK, int );  //压栈
void traverse(PSTACK);    //遍历
bool pop(PSTACK pS,int * pVal);   //出栈
void clear(PSTACK pS);    //清空栈

int main(void)
{
    STACK S;  //STACK等价于struct Stack
    int val;
    init(&S);  //造出空栈

    push(&S, 1);  //压栈
    push(&S, 2);
    push(&S, 3);
    push(&S, 4);
    push(&S, 5);
    push(&S, 6);

    traverse(&S); //遍历输出
/*
    if(pop(&S,&val))
    {
        printf("出栈成功，出栈的元素是%d\n", val);
    }
    else
    {
        printf("出栈失败！\n");
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
        printf("动态内存分配失败\n");
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
    PNODE pNew = (PNODE)malloc(sizeof(NODE));  //创建新的节点
    pNew->data = val;  //将val的值赋给新节点的数据域
    pNew->pNext = pS->pTop; //将新节点的指针域指向下一个节点.pS->Top不能改写成pS->Bottom
    pS->pTop = pNew; //pTop指向新节点
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

//清空栈
void clear(PSTACK pS)
{
    if(empty(pS))        //如果
    {
        return;
    }
    else
    {
        PNODE p = pS->pTop;  //定义元素p指向栈顶元素
        PNODE q = NULL;     //定义元素q，初始值为空

        while(p !=pS->pBottom)    //如果栈不为空
        {
            q = p->pNext;        //q指向p的下一个元素
            free(p);            //释放p所指向的栈顶元素
            p = q;               //将q所指向的元素赋给p
        }
        pS->pTop = pS->pBottom;
    }
}
