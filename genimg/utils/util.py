import torchvision
import os
import torch

def save_checkpoint(model, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    torch.save(model.state_dict(), path)

def log_images(noise, output, target, writer, step):
    grid = torchvision.utils.make_grid(torch.cat([noise, output, target], dim=0), nrow=noise.size(0))
    writer.add_image("Samples", grid, step)