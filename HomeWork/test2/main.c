// consumer2.c
#include<stdio.h>
#include<unistd.h>
#include<semaphore.h>
#include<fcntl.h>

#define SEM_B "goods_b"

int main()
{

        sem_t * pSemB = sem_open(SEM_B, O_CREAT, 0666, 10);
        int semVal;

        while(1)
        {
                sem_wait(pSemB);
                sem_getvalue(pSemB, &semVal);
                printf("%d\n",semVal);
                usleep(500000);
        }
        sem_close(pSemB);
        sem_unlink(SEM_B);
        return 0;
}
