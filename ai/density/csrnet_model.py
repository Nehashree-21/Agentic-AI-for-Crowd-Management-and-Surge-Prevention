import torch
import torch.nn as nn
from torchvision import models


class CSRNet(nn.Module):

    def __init__(self):
        super().__init__()

        self.frontend_feat = [
            64, 64, "M",
            128, 128, "M",
            256, 256, 256, "M",
            512, 512, 512
        ]

        self.backend_feat = [
            512, 512, 512,
            256, 128, 64
        ]

        self.frontend = self.make_layers(
            self.frontend_feat
        )

        self.backend = self.make_layers(
            self.backend_feat,
            in_channels=512,
            dilation=True
        )

        self.output_layer = nn.Conv2d(
            64,
            1,
            kernel_size=1
        )

    def forward(self, x):

        x = self.frontend(x)
        x = self.backend(x)
        x = self.output_layer(x)

        return x

    @staticmethod
    def make_layers(
        cfg,
        in_channels=3,
        dilation=False
    ):

        layers = []

        dilation_rate = 2 if dilation else 1

        for value in cfg:

            if value == "M":

                layers.append(
                    nn.MaxPool2d(
                        kernel_size=2,
                        stride=2
                    )
                )

            else:

                conv = nn.Conv2d(
                    in_channels,
                    value,
                    kernel_size=3,
                    padding=dilation_rate,
                    dilation=dilation_rate
                )

                layers.append(conv)
                layers.append(
                    nn.ReLU(inplace=True)
                )

                in_channels = value

        return nn.Sequential(*layers)