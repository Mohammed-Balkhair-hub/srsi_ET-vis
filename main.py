"""
srsi_ET-vis — optional Manim entry.

Prefer:
    manim -pqh topics/cnn/theory/convolution.py ConvolutionMath

Or:
    manim -pqh main.py WhyCNNs
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "topics" / "cnn"))

from theory.why_cnn import WhyCNNs
from theory.convolution import ConvolutionMath
from theory.padding_stride import PaddingAndStride
from theory.pooling import Pooling
from theory.architecture import CNNPipeline

__all__ = [
    "WhyCNNs",
    "ConvolutionMath",
    "PaddingAndStride",
    "Pooling",
    "CNNPipeline",
]
