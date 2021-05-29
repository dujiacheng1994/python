import torch as t
import torch.nn as nn
import torch.nn.functional as F
from torch import optim
import torchvision as tv
import torchvision.transforms as transforms
from torchvision.transforms import ToPILImage
import torchsnooper

transforms = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))])  #定义数据下载后处理方式
trainset = tv.datasets.CIFAR10(root='/home/cy/data/',train=True,download=True,transform=transforms)
testset = tv.datasets.CIFAR10('/home/cy/data/',train=False,download=True,transform=transforms)
trainloader = t.utils.data.DataLoader(trainset,batch_size = 4,shuffle = True,num_workers = 0)
testloader = t.utils.data.DataLoader(testset,batch_size=4,shuffle=False,num_workers=0)


classes = ('plane','car','bird','cat','deer','dog','from','horse','ship','truck')
(data,label)=trainset[100]
print(classes[label])
ToPILImage()((data+1)/2).resize((100,100))
dataiter = iter(trainloader)
images,labels = dataiter.next()
print(''.join('%10s' % classes[labels[j]] for j in range(4)))   #join不一定要是序列list，generator也可,generator是个函数！
ToPILImage()(tv.utils.make_grid((images+1)/2)).resize((80*4,80))



#正式代码
from torch import nn
import torch as t
from torch.nn import functional as F
from torchvision import models


class ResidualBlock(nn.Module):
    def __init__(self, inchannel, outchannel, stride=1,shortcut=None):
        super(ResidualBlock,self).__init__()
        self.left = nn.Sequential(
            nn.Conv2d(inchannel,outchannel,3,stride,1,bias=False),
            nn.BatchNorm2d(outchannel),
            nn.ReLU(inplace=True),
            nn.Conv2d(outchannel,outchannel,3,1,1,bias = False),
            nn.BatchNorm2d(outchannel)
        )
        self.right = shortcut

    def forward(self,x):
        out = self.left(x)
        residual = x if self.right is None else self.right(x)
        out += residual
        return F.relu(out)


class ResNet(nn.Module):
    def __init__(self,num_classes=1000):
        super(ResNet, self).__init__()
        self.pre = nn.Sequential(
            nn.Conv2d(3, 64, 7, 2, 4, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3,2,1)
        )
        self.layer1 = self._make_layer(64, 128, 3)
        self.layer2 = self._make_layer(128, 256, 4, stride=2)
        self.layer3 = self._make_layer(256, 512, 6, stride=2)
        self.layer4 = self._make_layer(512, 512, 3, stride=2)
        self.fc = nn.Linear(512,num_classes)

    def _make_layer(self,inchannel,outchannel,block_num,stride=1):
        shortcut = nn.Sequential(
            nn.Conv2d(inchannel,outchannel,1,stride,bias=False),
            nn.BatchNorm2d(outchannel)
        )
        layers = []  #多个ResidualBlock的列表
        layers.append(ResidualBlock(inchannel,outchannel,stride,shortcut))
        for i in range(1,block_num):
            layers.append(ResidualBlock(outchannel,outchannel))
        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.pre(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = F.avg_pool2d(x,7)
        x = x.view(x.size(0),-1)
        return self.fc(x)


net = ResNet()
#net = models.resnet34()
input = t.randn(1,3,224,224)
o = net(input)
print(net)
#正式代码

#Todo:此处要分两次运行！
criterion = nn.CrossEntropyLoss()
#optimizer = optim.SGD(net.parameters(),lr=0.001,momentum=0.9)
optimizer = optim.Adam(net.parameters())
for epoch in range(10):
    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):  # 适用于没有len的情况，如迭代器，生成器。 从0开始，每个trainloader的对象x[i]会变成（i,x[i]）
        inputs, labels = data
        optimizer.zero_grad()
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward(create_graph=True)
        optimizer.step()

        running_loss += loss.item()
        if i % 2000 == 1999:
            print('[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss / 2000))
            running_loss = 0.0
print('Finished Training')

dataiter = iter(testloader)
images,labels = dataiter.next()
print('实际的label:',''.join('%08s' % classes[labels[j]] for j in range(4)))
#ToPILImage()(tv.utils.make_grid(images/2-0.5)).resize((400,100))

outputs = net(images)
_,predicted = t.max(outputs.data,1)
print('预测结果:',''.join('%5s' % classes[predicted[j]] for j in range(4)))

correct = 0
total = 0
for data in testloader:
    images,labels = data
    outputs = net(images)
    _,predicted = t.max(outputs.data,1)
    total += labels.size(0)
    correct += (predicted == labels).sum()
print('10000张测试集中的准确率为：%d %%' % (100*correct/total))
