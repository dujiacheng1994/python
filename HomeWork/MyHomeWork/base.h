#ifndef BASE_H
#define BASE_H
#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
struct Base
{ size_t size;
   void * (* ctor) (void * self, va_list * app);
   void * (* dtor) (void * self);
   void (* draw) (const void * self);
};
#endif
