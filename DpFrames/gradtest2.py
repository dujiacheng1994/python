import torch

# 只要将Tensor类的requires_grad设成True
# 就会为这些节点构建计算图
x = torch.tensor(data_x, requires_grad=True)
W_x = torch.tensor(data_wx, requires_grad=True)
h = torch.tensor(data_h, requires_grad=True)
W_h = torch.tensor(data_wh, requires_grad=True)


i2h = torch.mm(W_x, x.t())
h2h = torch.mm(W_h, h.t())

next_h = h2h + i2h

next_next_h = next_h.tanh()

next_next_h.backward()