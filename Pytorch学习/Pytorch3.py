import torch as t
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):  #此处纯论继承!
    def __init__(self):    #此处才是需要输入的参数(self)
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)  #输入通道为3，输出通道为6(训练6个不同的卷积核/过滤器，每个)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
    def forward(self, x):
        print("1")
        print(x.size()) #[1,1,32,32] = [sample,channel,width,height]
        x=F.relu(self.conv1(x))   #32-4=28,卷积核为5,故减4
        print(x.size())
        x = F.max_pool2d(x, kernel_size=(2, 2)) #二维尺寸折半
        print(x.size())
        x = F.relu(self.conv2(x))
        print(x.size())
        x = F.max_pool2d(x, kernel_size=2)
        print(x.size())
        x = x.view(x.size()[0], -1)
        print(x.size())
        x = F.relu(self.fc1(x))
        print(x.size())
        x = F.relu(self.fc2(x))
        print(x.size())
        x = self.fc3(x)
        print(x.size())  #[1,10] 1个sample
        return x


net = Net()
print(net)
input = t.randn(1,1,32,32)
out = net.forward(input)

net.zero_grad()
out.backward(t.ones(1,10))
output = net(input)  #等效于forward

output = t.squeeze(output)  #!!!

target = t.arange(0,10)
criterion = nn.MSELoss()
loss = criterion(output,target.float())