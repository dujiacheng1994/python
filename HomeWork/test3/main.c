// producer.c
#include<stdio.h>
#include<unistd.h>
#include<semaphore.h>
#include<fcntl.h>

#define SEM_A "goods_a"
#define SEM_B "goods_b"

#define BUFFER_SIZE 20
int main()
{
        sem_t * pSemA = sem_open(SEM_A, O_CREAT, 0666, 10);
        sem_t * pSemB = sem_open(SEM_B, O_CREAT, 0666, 10);
        int semVal;
//      for(int i=0;i<20;i++)
        while(1)
        {
                sem_getvalue(pSemA, &semVal);
                if(semVal < BUFFER_SIZE)
                {
                        usleep(600000);
                    // ��Ҫ��sleep������delay��delay���ɱ���ϣ���sleep������
                        sem_post(pSemA);  //V����
                        printf("Number of Goods A: %d\n",semVal);
                }
                sem_getvalue(pSemB, &semVal);
                if(semVal < BUFFER_SIZE)
                {
                        usleep(600000);
                        sem_post(pSemB);
                        printf("Number of Goods B: %d\n",semVal);
                }
        }
        sem_close(pSemA);
        sem_close(pSemB);
        return 0;
}
