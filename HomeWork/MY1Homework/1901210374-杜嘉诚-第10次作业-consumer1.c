// consumer1.c
#include<stdio.h>
#include<unistd.h>
#include<semaphore.h>
#include<fcntl.h>

#define SEM_A "goods_a"

int main()
{

        sem_t * pSemA = sem_open(SEM_A, O_CREAT, 0666, 10);
        int semVal;

        while(1)
        {
                sem_wait(pSemA);
                sem_getvalue(pSemA, &semVal);
                printf("%d\n",semVal);
                usleep(500000);
        }
        sem_close(pSemA);
        sem_unlink(SEM_A);
        return 0;
}
