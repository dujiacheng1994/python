#include<iostream>
#include<cmath>
#include<cstdio>
using namespace std;
//����CShape
class CShape{
public:
    virtual double Area(){};
};
//������Triangle
class CTriangle:public CShape{
public:
    double a,b,c;
    virtual double Area();
};
double CTriangle::Area(){
    double p=(a+b+c)/2.0;
    return sqrt(p*(p-a)*(p-b)*(p-c));
}
//������CRectangle
class CRectangle:public CShape{
public:
    double w,h;
    virtual double Area();
};
double CRectangle::Area(){
    return w*h;
}
//������CCircle
class CCircle:public CShape{
public:
    double r;
    virtual double Area();
};
double CCircle::Area(){
    double pi=3.14;
    return pi*r*r;
}
int main()
{
    CShape* p[3];
    CTriangle* pt1=new CTriangle();
    CRectangle* pt2=new CRectangle();
    CCircle* pt3=new CCircle();
    cin>>pt1->a>>pt1->b>>pt1->c;
    cin>>pt2->w>>pt2->h;
    cin>>pt3->r;
    //ͳһ��CShape����ָ�룬��ʾ��̬
    p[0]=pt1;
    p[1]=pt2;
    p[2]=pt3;
    printf("Triangle:%lf\n",p[0]->Area());
    printf("Rectangle:%lf\n",p[1]->Area());
    printf("Circle:%lf\n",p[2]->Area());

    return 0;
}
