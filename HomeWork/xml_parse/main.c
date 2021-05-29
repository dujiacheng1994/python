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

typedef struct bcs_t{           //对每个检测出来的符号<会创一个信息结构体
     int fileoffset;            //块偏移量,以char为单位
     int bt;                    //符号类型
}Bcs;
typedef struct node
{
    int bufnum;
    char data[BUFLEN];
    Bcs bcs[BUFLEN/10];
    struct node *next;
}node;
void stage1(node* mynode){       //解析每个<符号
    int i=0;
    char* p = mynode->data;      //字符指针遍历data
    int cnt=0;
    for(i=0;i<BUFLEN;i++){
        if(*p == '<'){
            mynode->bcs[cnt].fileoffset = i;
        }
    }
    printf("%d",cnt);
}
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
    stage1(head->next);
    //²âÊÔÁ´±í
//    while(head!=NULL){
//        printf("%d ",head->bufnum);
//        head = head->next;
//    }


    return 0;
}


