#include <stdio.h>
#include <stdlib.h>
#define BUFLEN 10240
//typedef enum Bcstype{
//      StagorEmptytag_start,
//      Etag_start,
//      PI_start,
//      Content,
//      CDSECT_start,
//      COMMENT_start
//}Bcstype;

//typedef struct buffer_t{
//    char buf[BUFLEN];
//    Bcsarray bcsay;
//    int bufnum;
//    int FINISH_STAGE0;
//    int START_STAGE0;
//    int FINISH_STAGE1;
//    int FINISH_STAGE2;
//    int FINISH_STAGE3;
//    int START_STAGE1;
//    int START_STAGE2;
//    int START_STAGE3;
//    Struct buffer_t *next;
//}databuf;

//对每个检测出来的符号<会创一个信息结构体
typedef Struct bcs_t{
     int fileoffset; //块偏移量
     int bufnum;  //所在块号
     int bufpos;  //所在块偏移量
     int bt;    //符号类型
}Bcs;
//数据<信息链表结点, 每个块的<信息存入bcs数组里,而node_t与node一一对应
typedef struct node_t{
   Bcs bcs[BUFLEN/10];
   struct node_t *next;
} node_t;
//数据缓冲区链表结点
typedef struct node
{
    int bufnum;
    char data[BUFLEN];
    struct node *next;
}node;
int main(void){
    FILE *fp;
    int i=0;
    if((fp = fopen("test.xml", "rb")) == NULL)
        printf("can't open the file! \n");
    node* head = (node*)malloc(sizeof(node));
    head->bufnum = -1;
    head->next = NULL;
    node *pre = head;
    while(!feof(fp)){
        node* p=(node*)malloc(sizeof(node));
        p->bufnum = i++;
        fread(p->data,sizeof(char),BUFLEN,fp);
        pre->next = p;
        p->next = NULL;
        pre = p;
    }
    //²âÊÔÁ´±í
//    while(head!=NULL){
//        printf("%d ",head->bufnum);
//        head = head->next;
//    }


    return 0;
}


