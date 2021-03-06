import numpy as np
import pytest
import scipy.interpolate
import torch

from candlelight.functional import cubic

test_params = [
    (np.linspace(0.1, 0.9, 12), np.array([1, 4, 6, 9]), (0, 1)),
    (np.linspace(0, 1, 100), np.arange(100), (0, 1)),
    (np.linspace(2.6, 5, 14), np.array([6, 1, 2.4, 3.2]), (2, 5)),
    (np.linspace(1, 2, 36).reshape(6, 6), np.array([0.1, 0.3, 0.2, 0.5, 0.7]), (0, 2)),
    (np.linspace(0.1, 0.9, 12), np.array([0.1, 0.5, 2, -0.5, 0.7]), (0, 1)),
]


@pytest.mark.parametrize('input, value, domain', test_params)
def test_cubic(input, value, domain):
    x = np.linspace(domain[0], domain[1], value.size)
    spline = scipy.interpolate.CubicSpline(x, value, bc_type='natural')
    numpy_result = spline(input)

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    input_tensor = torch.tensor(input, dtype=torch.float32, device=device)
    node_tensor = torch.tensor(value, dtype=torch.float32, device=device)
    torch_result = cubic(input_tensor, node_tensor, domain).cpu().numpy()
    assert np.allclose(numpy_result, torch_result)
