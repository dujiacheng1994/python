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




typedef enum XMLEventLabel_t
{
	STAG = 1,
	ETAG = 2,
	PI = 3,
	COMMENT = 4,
	CDATA = 5
}XMLEventLabel;

typedef enum ErrorValue_t
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
	XMLEventLabel i_label;
	char *p_event_start;
	int64_t i_event_length;

	char *event_stream;
	int64_t i_event_stream_length;
}XMLEvents;

typedef struct XMLDataSet_t
{
	char *p_start_data_set;
	int64_t i_data_set_length;
	XMLEvents *events[MAX_COUNT_EVENTS];//TODO: use realloc to avoid static array length
	int64_t i_events;

	char *XMLstream;
	int64_t XMLstream_length;
}XMLDataSet;

typedef struct XMLSTagStack_t
{
	int dataset_index;
	int event_index;
	struct XMLSTagStack_t *next;
}XMLSTagStack;

typedef struct XMLParserContext_t
{
	FILE *XMLfilein;
	FILE *XMLstreamout;
	char *XMLbuf;
	int64_t XMLlength;

	int64_t i_count_data_sets;
	XMLDataSet *pp_data_sets[MAX_COUNT_DATA_SETS];

	//multi-thread
	int64_t i_parse;
	int64_t i_post;
	//int unresolved_stag_num;
	XMLSTagStack* unresolved_stag_stack_head;
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
