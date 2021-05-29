#include "new.h"
#include "base.h"
void *new(const void * _base, int a, int b)
{
    struct Base *base = _base;
    void * p = calloc(1, base->size);
    (struct Base*) p= base;
    if (base ->ctor)
    {
        va_list ap;
        va_start(ap,_base);
        p=base->ctor(p,&ap);
        va_end(ap);
    }
    return p;
}
void delete (void * self)
{
    const struct Base * cp = self;
    if (self &&  cp && cp -> dtor)
    self = cp ->dtor(self);
    free(self);
}
void draw (const void * self)
{
    const struct Base * cp = self;
    assert(self && cp && cp->draw);
    cp ->draw(self);
}

