#测试1
import torch as t
def f(x):
    """x^2 * e^x"""
    y = x ** 2 * t.exp(x)
    return y
def gradf(x):
    """2*x*e^x + x^2*e^x"""
    dx = 2 * x * t.exp(x) + x ** 2 * t.exp(x)
    return dx
x = t.randn((3, 4),requires_grad=True)
y = f(x)
y.backward(t.ones(y.size()))
print(x.grad)
print(gradf(x))

#测试2
import torch as t
def g(x1,x2,x3):
    y=x1*x2*x3
    return y
x1 = t.randn((3, 4),requires_grad=True)
x2 = t.randn((3, 4),requires_grad=True)
x3 = t.randn((3, 4),requires_grad=True)
y = g(x1,x2,x3)
y.backward(t.ones(y.size()))

#测试3
import torch as t
def f(x):   #定义y=f(x)则定义了计算图，即y的grad_fn一直到叶节点x
    """x^2 * e^x"""
    y = x ** 2 * t.exp(x) + x**3 * t.sin(x)
    return y

x = t.randn((3, 4),requires_grad=True)
y = f(x)   #类比正向传播，此处实例化了y与x的关联,是之后对y求backward能体现到x.grad的原因
y.backward(t.ones(y.size()))   #求y对x的偏导，记录在x.grad里而非y里
print(x.grad)
print(gradf(x))

