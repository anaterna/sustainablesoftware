import torch
import time
from torchvision import transforms
from torchvision.models import resnet50, ResNet50_Weights

torch.manual_seed(0)
torch.cuda.manual_seed(0)
torch.cuda.manual_seed_all(0)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False


device = 'cpu'
if torch.cuda.is_available():
   device = 'cuda'
   
print('Using {} device'.format(device))


resnet = resnet50(weights=ResNet50_Weights.DEFAULT)
resnet.to(device)
resnet.eval()

input_sizes = [2 ** x for x in range(8,12)]
print(input_sizes)

preprocess = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

for u,input_size in enumerate(input_sizes):
    #number of inferences
    iters = int(400/(u+1))

    #create a random image
    image_test = torch.rand(1,3,input_size,input_size)
    image_test = preprocess(image_test)
    image_test = image_test.to(device)


    print(f'Experiment is running for image size {input_size}x{input_size}')
    start_xp = time.time()

    for t in range(iters):
        y = resnet(image_test)
        
    end_xp = time.time()
    print(f"Experiment took {end_xp-start_xp} seconds")
