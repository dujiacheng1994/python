import torch as t
from torch import nn


class Linear(nn.Module):
    def __init__(self,in_features,out_features):
        super(Linear,self).__init__()
        self.w = nn.Parameter(t.randn(in_features,out_features))
        self.b = nn.Parameter(t.randn(out_features))

    def forward(self, x):
        x = x.mm(self.w)
        return x + self.b.expand_as(x)


layer = Linear(4,3)
input = t.randn(2,4)
output = layer(input)
print(output)

#全连接层
input = t.randn(2,3)    #标准正态分布，2个sample,长度3
linear = nn.Linear(3,4)
h = linear(input)
#BatchNorm层
bn = nn.BatchNorm1d(4)
bn.weight.data = 4 * t.ones(4)
print(bn.weight.data)
bn.bias.data = t.zeros(4)
print(bn.bias.data)
bn_out = bn(h)
#Dropout层，一半的数变0
dropout = nn.Dropout(0.5)
o = dropout(bn_out)