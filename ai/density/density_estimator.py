import cv2
import numpy as np
import torch

from huggingface_hub import hf_hub_download

from ai.density.csrnet_model import CSRNet


class CrowdDensityEstimator:

    def __init__(self):

        print("Loading CSRNet crowd-density model...")

        weights_path = hf_hub_download(
            repo_id="AbdurRahman011/csrnet-indian-metro-crowd-density",
            filename="csrnet_v3_best.pth"
        )

        self.device = torch.device("cpu")

        self.model = CSRNet()

        checkpoint = torch.load(
            weights_path,
            map_location=self.device
        )

        if isinstance(checkpoint, dict) and "state_dict" in checkpoint:
            checkpoint = checkpoint["state_dict"]

        self.model.load_state_dict(
            checkpoint,
            strict=True
        )

        self.model.to(self.device)
        self.model.eval()

        print("CSRNet loaded successfully.")

    def preprocess(self, frame):

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        image = rgb.astype(
            np.float32
        ) / 255.0

        mean = np.array(
            [0.485, 0.456, 0.406],
            dtype=np.float32
        )

        std = np.array(
            [0.229, 0.224, 0.225],
            dtype=np.float32
        )

        image = (
            image - mean
        ) / std

        tensor = torch.from_numpy(
            image
        ).permute(
            2, 0, 1
        ).unsqueeze(0)

        return tensor.float()

    def estimate(self, frame):

        input_tensor = self.preprocess(frame)

        with torch.no_grad():

            density_map = self.model(
                input_tensor
            )

        density = density_map.squeeze().cpu().numpy()

        count = float(
            np.maximum(
                density,
                0
            ).sum()
        )

        return count, density