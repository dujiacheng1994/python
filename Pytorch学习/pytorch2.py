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
trainloader = t.utils.data.DataLoader(trainset,batch_size = 4,shuffle = True,num_workers = 2)
testloader = t.utils.data.DataLoader(testset,batch_size=4,shuffle=False,num_workers=2)


classes = ('plane','car','bird','cat','deer','dog','from','horse','ship','truck')
(data,label)=trainset[100]
print(classes[label])
ToPILImage()((data+1)/2).resize((100,100))
dataiter = iter(trainloader)
images,labels = dataiter.next()
print(''.join('%10s' % classes[labels[j]] for j in range(4)))   #join不一定要是序列list，generator也可,generator是个函数！
ToPILImage()(tv.utils.make_grid((images+1)/2)).resize((80*4,80))


class Net1(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(x.size()[0], -1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
class Net2(nn.module):
    def __init__(self):
        super(Net2,self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3,6,5),
            nn.ReLU(),
            nn.MaxPool2d(2,2),
            nn.Conv2d(6,16,5),
            nn.ReLU(),
            nn.MaxPool2d(2,2)
        )
        self.classifier = nn.Sequential(
            nn.Linear(16*5*5,120),
            nn.ReLU(),
            nn.Linear(120,84),
            nn.ReLU(),
            nn.Linear(84,10)
        )
    def forward(self,x):
        x = self.features(x)
        x = x.view(-1,16*5*5)
        x = self.classifier(x)
        return x
net = Net1()
print(net)

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

