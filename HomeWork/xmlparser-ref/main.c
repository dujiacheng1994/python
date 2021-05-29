#include "common.h"
#include "file_io.h"
#include "parse_event.h"
#include "post_process.h"


void pipe_send(stage_t *stage)          //����һ�׶η��Ϳ��Կ�ʼ����Ϣ
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

void pipe_stage(void *arg)             //��Ҫ�����������׶εľ��崦��
{
	stage_t *stage = (stage_t*)arg;
	stage_t *next_stage = stage->next;
	XMLParserContext *h = stage->h;

	pthread_mutex_lock(&stage->mutex); //���׶δ�������û���������
	if (stage->stage_ID == 1)          //��һ�׶Σ��¼�����
	{
		int64_t i;
		char *pdata;
		pdata = h->XMLbuf;             //ȫ��ָ��
		i = 0;
		h->i_count_data_sets = 0;
		error_state = 0;
		while (i < h->XMLlength)
		{
			XMLDataSet *dataset = (XMLDataSet *)malloc(sizeof(XMLDataSet));     //�˴�dataset���¼�������
			memset(dataset, 0, sizeof(XMLDataSet));
			//when the rest is no more than max, deal in a separate way.
			if (h->XMLlength - i < DATA_SET_MAX)
			{
				divide_event_edge(dataset, pdata, h->XMLlength - i);            //���ֵ����һ�����ݿ飬���⴦��
				i = h->XMLlength;
			}
			else
			{
				int64_t eventlen = divide_event(dataset, pdata);                //���ݿ��л����¼�
				pdata += eventlen;
				i += eventlen;
			}
			h->pp_data_sets[h->i_count_data_sets++] = dataset;
			printf("divide XML %d\n", h->i_count_data_sets);
			pipe_send(next_stage);              //�������ݻ�����ɣ�������һ�׶�
		}
		pipe_send(next_stage);
	}
	else if (stage->stage_ID == 2)              //�ڶ��׶Σ��¼�����
	{
		while (1)
		{
			while (stage->data_ready != 1)      //����������ݵĵ�һ�׶�δ�����
			{
				pthread_cond_wait(&stage->avail, &stage->mutex);
			}
			if (h->i_parse == h->i_count_data_sets)
				break;
			parse_events(h);                    //�¼���������
			h->i_parse++;
			printf("parse XML %d\n", h->i_parse);
			pipe_send(next_stage);
			stage->data_ready = 0;
			pthread_cond_signal(&stage->ready);
		}
		pipe_send(next_stage);
	}
	else            //�����׶Σ�����
	{
		while (1)
		{
			while (stage->data_ready != 1)
			{
				pthread_cond_wait(&stage->avail, &stage->mutex);
			}
			if (h->i_post == h->i_count_data_sets)
				break;
			post_process(h);        //������
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
	stage_t **link = &pipe->head, *new_stage, *stage;               //����3���׶ε��̱߳�ʶ

	pthread_mutex_init(&pipe->mutex, NULL);
	pipe->stages = stages;
	pipe->active = 0;

	for (pipe_index = 0; pipe_index < stages; pipe_index++)         //��ʼ�����߳̿��Ʊ���
	{
		new_stage = (stage_t*)malloc(sizeof(stage_t));
		pthread_mutex_init(&new_stage->mutex, NULL);                //��ʼ������������������ֻ��һ�����̶�д
		pthread_cond_init(&new_stage->avail, NULL);                 //��ʼ��������������֤�����ѱ����ֲſ�ʼ����
		pthread_cond_init(&new_stage->ready, NULL);                 //��ʼ��������������֤�����ѱ������ſ�ʼ����
		new_stage->data_ready = 0;
		new_stage->h = _h;
		new_stage->stage_ID = pipe_index + 1;
		*link = new_stage;
		link = &new_stage->next;
	}
	*link = (stage_t*)NULL;
	for (stage = pipe->head; stage != NULL; stage = stage->next)
	{
		pthread_create(&stage->thread, NULL, pipe_stage, (void*)stage);     //�������׶��̣߳�����pipe_stage����
	}
	return 0;
}

void pthread_destroy(pipe_t pipeline)   //�����������˳������й��߳�
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
	XMLParserContext *h;                    //XML����������
	pipe_t pipeline;                        //�׶�ָʾ��stage��������
	struct timeval start, end;
	double timeuse;
	gettimeofday(&start, NULL);
	if(argc != 3)                           //������
	{
		printf("error input args\n");
		return 0;
	}
	h = read_XML_file(argv[1]);             //�����ļ�
	if (h == NULL)
		return 0;
	h->i_parse = 0;
	h->i_post = 0;

	pipe_create(&pipeline, 3, h);                           //��Ҫ����Ҫ������ڣ���ʼ����
	pthread_join(pipeline.head->thread, NULL);              //�ȴ�divide�߳̽���
	pthread_join(pipeline.head->next->thread, NULL);        //�ȴ�parse�߳̽���
	pthread_join(pipeline.head->next->next->thread, NULL);  //�ȴ�post_process�߳̽���
	release_XML_file(h, argv[2]);                           //��������ʾ������ɣ���������ļ�
	pthread_destroy(pipeline);                              //�˳��й��߳�

	gettimeofday(&end, NULL);                               //������ʱ
	timeuse  = 1000000 * (end.tv_sec - start.tv_sec) + end.tv_usec - start.tv_usec;
	timeuse /= 1000;
	printf("%.4lf ms time used\n", timeuse);
	return 0;
}
