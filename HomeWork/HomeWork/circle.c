#include "circle.h"
#include "new.h"
#include "base.h"
#include "point.c"
struct Circle{
    struct Point point;
    int radius;
};
static void *Circle_ctor (void *_self,va_list *app){
    struct Circle *self = _self;
    self->point.x = va_arg(*app, int);
    self->point.y = va_arg(*app, int);
    self->radius = va_arg(*app, int);
    return self;
}
static void Circle_draw (const void *_self)
{
    struct Circle *self_c = _self;
    struct Point *self_p=&self_c->point;
    printf("Circle draw Point (%d,%d),Radius %d", self_p->x, self_p->y, self_c->radius);
}
static const struct Base _Circle = {
    sizeof(struct Circle), Circle_ctor, 0, Circle_draw
};
const void * Circle = & _Circle;


