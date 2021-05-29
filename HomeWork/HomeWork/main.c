#include "point.h"
#include "new.h"
#include "circle.h"
int main (int argc, char ** argv)
{
    void * p = new(Point, 1, 2);
    void * pp = new(Circle, 1, 2);
    draw(p);
    draw(pp);
    delete(p);
    delete(pp);
}
