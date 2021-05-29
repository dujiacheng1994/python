#include "common.h"
#include "file_io.h"
#include "parse_event.h"
#include "post_process.h"


void pipe_send(stage_t *stage)          //给下一阶段发送可以开始的消息
{
	pthread_mutex_lock(&stage->mutex);
	/*
	* If there's data in the pipe stage, wait for it
	* to be consumed.
	*/
	while (stage->data_ready)
	{
		pthread_cond_wait(&stage->ready, &stage->mutex);
	}

	/*
	* Send the new data
	*/
	stage->data_ready = 1;
	pthread_cond_signal(&stage->avail);
	pthread_mutex_unlock(&stage->mutex);
}

void pipe_stage(void *arg)             //主要函数！三个阶段的具体处理
{
	stage_t *stage = (stage_t*)arg;
	stage_t *next_stage = stage->next;
	XMLParserContext *h = stage->h;

	pthread_mutex_lock(&stage->mutex); //三阶段处理过程用互斥锁锁上
	if (stage->stage_ID == 1)          //第一阶段：事件划分
	{
		int64_t i;
		char *pdata;
		pdata = h->XMLbuf;             //全文指针
		i = 0;
		h->i_count_data_sets = 0;
		error_state = 0;
		while (i < h->XMLlength)
		{
			XMLDataSet *dataset = (XMLDataSet *)malloc(sizeof(XMLDataSet));     //此处dataset是事件池数组
			memset(dataset, 0, sizeof(XMLDataSet));
			//when the rest is no more than max, deal in a separate way.
			if (h->XMLlength - i < DATA_SET_MAX)
			{
				divide_event_edge(dataset, pdata, h->XMLlength - i);            //划分到最后一个数据块，特殊处理
				i = h->XMLlength;
			}
			else
			{
				int64_t eventlen = divide_event(dataset, pdata);                //数据块中划分事件
				pdata += eventlen;
				i += eventlen;
			}
			h->pp_data_sets[h->i_count_data_sets++] = dataset;
			printf("divide XML %d\n", h->i_count_data_sets);
			pipe_send(next_stage);              //所有数据划分完成，进入下一阶段
		}
		pipe_send(next_stage);
	}
	else if (stage->stage_ID == 2)              //第二阶段：事件解析
	{
		while (1)
		{
			while (stage->data_ready != 1)      //如果所有数据的第一阶段未已完成
			{
				pthread_cond_wait(&stage->avail, &stage->mutex);
			}
			if (h->i_parse == h->i_count_data_sets)
				break;
			parse_events(h);                    //事件解析函数
			h->i_parse++;
			printf("parse XML %d\n", h->i_parse);
			pipe_send(next_stage);
			stage->data_ready = 0;
			pthread_cond_signal(&stage->ready);
		}
		pipe_send(next_stage);
	}
	else            //第三阶段：后处理
	{
		while (1)
		{
			while (stage->data_ready != 1)
			{
				pthread_cond_wait(&stage->avail, &stage->mutex);
			}
			if (h->i_post == h->i_count_data_sets)
				break;
			post_process(h);        //后处理函数
			h->i_post++;
			//printf("post XML %d\n", h->i_post);
			stage->data_ready = 0;
			pthread_cond_signal(&stage->ready);
		}
	}
	pthread_mutex_unlock(&stage->mutex);
}

int pipe_create(pipe_t *pipe, int stages, XMLParserContext *_h)
{
	int pipe_index;
	stage_t **link = &pipe->head, *new_stage, *stage;               //创建3个阶段的线程标识

	pthread_mutex_init(&pipe->mutex, NULL);
	pipe->stages = stages;
	pipe->active = 0;

	for (pipe_index = 0; pipe_index < stages; pipe_index++)         //初始化各线程控制变量
	{
		new_stage = (stage_t*)malloc(sizeof(stage_t));
		pthread_mutex_init(&new_stage->mutex, NULL);                //初始化互斥锁，保护数据只有一个进程读写
		pthread_cond_init(&new_stage->avail, NULL);                 //初始化条件变量，保证数据已被划分才开始解析
		pthread_cond_init(&new_stage->ready, NULL);                 //初始化条件变量，保证数据已被解析才开始后处理
		new_stage->data_ready = 0;
		new_stage->h = _h;
		new_stage->stage_ID = pipe_index + 1;
		*link = new_stage;
		link = &new_stage->next;
	}
	*link = (stage_t*)NULL;
	for (stage = pipe->head; stage != NULL; stage = stage->next)
	{
		pthread_create(&stage->thread, NULL, pipe_stage, (void*)stage);     //启动各阶段线程，传入pipe_stage函数
	}
	return 0;
}

void pthread_destroy(pipe_t pipeline)   //解析后，用于退出所有有关线程
{
	pthread_cond_destroy(&pipeline.head->avail, NULL);
	pthread_cond_destroy(&pipeline.head->ready, NULL);
	pthread_mutex_destroy(&pipeline.head->mutex);
	pthread_cond_destroy(&pipeline.head->next->avail, NULL);
	pthread_cond_destroy(&pipeline.head->next->ready, NULL);
	pthread_mutex_destroy(&pipeline.head->next->mutex);
	pthread_cond_destroy(&pipeline.head->next->next->avail, NULL);
	pthread_cond_destroy(&pipeline.head->next->next->ready, NULL);
	pthread_mutex_destroy(&pipeline.head->next->next->mutex);
}

int main(int argc, char **argv)
{
	XMLParserContext *h;                    //XML解析上下文
	pipe_t pipeline;                        //阶段指示，stage结点的链表
	struct timeval start, end;
	double timeuse;
	gettimeofday(&start, NULL);
	if(argc != 3)                           //输入检查
	{
		printf("error input args\n");
		return 0;
	}
	h = read_XML_file(argv[1]);             //读入文件
	if (h == NULL)
		return 0;
	h->i_parse = 0;
	h->i_post = 0;

	pipe_create(&pipeline, 3, h);                           //重要！主要函数入口，开始解析
	pthread_join(pipeline.head->thread, NULL);              //等待divide线程结束
	pthread_join(pipeline.head->next->thread, NULL);        //等待parse线程结束
	pthread_join(pipeline.head->next->next->thread, NULL);  //等待post_process线程结束
	release_XML_file(h, argv[2]);                           //均结束表示解析完成，输出解析文件
	pthread_destroy(pipeline);                              //退出有关线程

	gettimeofday(&end, NULL);                               //计算用时
	timeuse  = 1000000 * (end.tv_sec - start.tv_sec) + end.tv_usec - start.tv_usec;
	timeuse /= 1000;
	printf("%.4lf ms time used\n", timeuse);
	return 0;
}
