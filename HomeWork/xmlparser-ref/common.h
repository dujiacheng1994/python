#ifndef COMMON_H
#define COMMON_H
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifndef __GNUC__
#include <stdint.h>
#include <pthread.h>
#else
#include <sys/types.h>
#include <sys/time.h>
#endif
#define DATA_SET_MAX 10240
#define MAX_COUNT_EVENTS 10000
#define MAX_COUNT_DATA_SETS 100000
#define Event_Stream_Size 1024
#define STAG_NAME_LEN 100
int error_state;

typedef enum XMLEventLabel_t    //“<”符号类型
{
	STAG = 1,
	ETAG = 2,
	PI = 3,
	COMMENT = 4,
	CDATA = 5
}XMLEventLabel;

typedef enum ErrorValue_t       //错误类型
{
	NoError = 0,
	MissElem = 1,    //miss <,\,.......
	NameStartCharError = 2,
	NameCharError = 3,
	AttributeError = 4,
	CommentStartError = 5,
	CommentError = 6,
	CharError = 7,
	PITargetError = 8,
	PIError = 9,
}ErrorValue;

typedef struct XMLEvents_t
{
	XMLEventLabel i_label;          //事件类型
	char *p_event_start;            //事件<偏移指针（首）
	int64_t i_event_length;         //原事件长度
	char *event_stream;             //事件输出流
	int64_t i_event_stream_length;  //事件输出流长度
}XMLEvents;

typedef struct XMLDataSet_t                     //事件池，正常容量为MAX_COUNT_EVENTS=10000，可扩展
{
	char *p_start_data_set;                     //数据块的首指针（在全文中）
	int64_t i_data_set_length;                  //数据块长度
	XMLEvents *events[MAX_COUNT_EVENTS];        //是*events指针的数组，存一堆<事件
	int64_t i_events;                           //数据块中事件数（<个数）
}XMLDataSet;

typedef struct XMLSTagStack_t
{
	int dataset_index;
	int event_index;
	struct XMLSTagStack_t *next;
}XMLSTagStack;

typedef struct XMLParserContext_t                   //对于读入的XML文件维护一个上下文
{
	FILE *XMLfilein;                                //xml输入文件指针
	FILE *XMLstreamout;                             //xml解析文件指针
	char *XMLbuf;                                   //xml全文存储
	int64_t XMLlength;                              //xml全文长度
	int64_t i_count_data_sets;                      //事件池数目
	XMLDataSet *pp_data_sets[MAX_COUNT_DATA_SETS];  //事件池链表，最多10000个（很难达到）（指针*pp_data_sets形态）
	//multi-thread
	int64_t i_parse;
	int64_t i_post;
	XMLSTagStack* unresolved_stag_stack_head;       //后处理用于检验SE EE匹配所用的栈头
}XMLParserContext;

typedef struct stage_tag {
	int stage_ID;                       /*1-divide 2-parse 3-post*/
	pthread_mutex_t     mutex;          /* Protect data */
	pthread_cond_t      avail;          /* Data available */
	pthread_cond_t      ready;          /* Ready for data */
	int                 data_ready;     /* Data present */
	XMLParserContext	*h;
	pthread_t           thread;         /* Thread for stage */
	struct stage_tag    *next;          /* Next stage */
} stage_t;

/*
* External structure representing the entire
* pipeline.
*/
typedef struct pipe_tag {
	pthread_mutex_t     mutex;          /* Mutex to protect pipe */
	stage_t             *head;          /* First stage */
	stage_t             *tail;          /* Final stage */
	int                 stages;         /* Number of stages */
	int                 active;         /* Active data elements */
} pipe_t;

#endif
