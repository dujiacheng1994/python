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

typedef enum XMLEventLabel_t    //��<����������
{
	STAG = 1,
	ETAG = 2,
	PI = 3,
	COMMENT = 4,
	CDATA = 5
}XMLEventLabel;

typedef enum ErrorValue_t       //��������
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
	XMLEventLabel i_label;          //�¼�����
	char *p_event_start;            //�¼�<ƫ��ָ�루�ף�
	int64_t i_event_length;         //ԭ�¼�����
	char *event_stream;             //�¼������
	int64_t i_event_stream_length;  //�¼����������
}XMLEvents;

typedef struct XMLDataSet_t                     //�¼��أ���������ΪMAX_COUNT_EVENTS=10000������չ
{
	char *p_start_data_set;                     //���ݿ����ָ�루��ȫ���У�
	int64_t i_data_set_length;                  //���ݿ鳤��
	XMLEvents *events[MAX_COUNT_EVENTS];        //��*eventsָ������飬��һ��<�¼�
	int64_t i_events;                           //���ݿ����¼�����<������
}XMLDataSet;

typedef struct XMLSTagStack_t
{
	int dataset_index;
	int event_index;
	struct XMLSTagStack_t *next;
}XMLSTagStack;

typedef struct XMLParserContext_t                   //���ڶ����XML�ļ�ά��һ��������
{
	FILE *XMLfilein;                                //xml�����ļ�ָ��
	FILE *XMLstreamout;                             //xml�����ļ�ָ��
	char *XMLbuf;                                   //xmlȫ�Ĵ洢
	int64_t XMLlength;                              //xmlȫ�ĳ���
	int64_t i_count_data_sets;                      //�¼�����Ŀ
	XMLDataSet *pp_data_sets[MAX_COUNT_DATA_SETS];  //�¼����������10000�������Ѵﵽ����ָ��*pp_data_sets��̬��
	//multi-thread
	int64_t i_parse;
	int64_t i_post;
	XMLSTagStack* unresolved_stag_stack_head;       //�������ڼ���SE EEƥ�����õ�ջͷ
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
