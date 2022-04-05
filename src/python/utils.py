import torch


def get_device() -> torch.device:
    """ Returns the device to use for training.

    Returns:
        torch.device: The device to use for training.
    """
    if torch.cuda.is_available():
        return torch.device("cuda")
    else:
        return torch.device("cpu")