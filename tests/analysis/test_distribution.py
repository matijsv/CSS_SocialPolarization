import pytest
import numpy as np
from scipy.signal import find_peaks
from src.core.utils import get_opinion_hist
from src.analysis.distribution import opinions_variance, count_peaks_in_histogram

@pytest.fixture
def mock_opinion_data():
    """Fixture to simulate opinion data returned by get_opinion_hist."""
    all_opinions = [
        [0.1, 0.2, 0.1, 0.3, 0.4],
        [0.15, 0.25, 0.12, 0.35, 0.45],
    ]
    bins = np.linspace(0, 1, 11)  # 10 bins
    histograms = [
        np.histogram(run, bins=bins)[0] for run in all_opinions
    ]
    average_histogram = np.mean(histograms, axis=0)
    return all_opinions, bins, average_histogram


@pytest.mark.parametrize("average_histogram, threshold, distance, expected_num_peaks", [
    ([0, 50, 200, 150, 50, 10, 0], 100, 1, 1),  # Two peaks above threshold
    ([0, 10, 20, 30, 40, 50], 60, 1, 0),        # No peaks above threshold
    ([0, 100, 200, 50, 200, 100, 0], 100, 1, 2),  # Three peaks
])
def test_count_peaks_in_histogram(average_histogram, threshold, distance, expected_num_peaks):
    """
    Test the peak counting in the opinion histogram.
    """
    num_peaks = count_peaks_in_histogram(average_histogram, threshold, distance)
    assert num_peaks == expected_num_peaks, (
        f"Expected {expected_num_peaks} peaks, but got {num_peaks}"
    )
