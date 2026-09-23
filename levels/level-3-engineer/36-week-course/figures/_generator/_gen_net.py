"""NETWORK motifs: one neuron, a layered network with shapes, forward vs backward.

Arithmetic is the hand-traced network from Module 5:
  x = [1.0, 2.0], w = [0.5, 0.8], b = 0.1 -> sum = 2.20 -> ReLU -> 2.20.
Shapes are the Module 5 shape trace: (750, 2) -> 16 hidden -> (750, 1).
"""
from _gen_core import *
import _gen_tensor  # noqa: F401  (registers the tensor motifs first)

# ================================================================== neuron
M("motif-neuron", "One neuron: multiply, add, squash",
  "Two input circles holding 1.0 and 2.0 feed into a circle labelled sum, along wires labelled times "
  "0.5 and times 0.8. A third wire brings in a bias of 0.1. The sum, 2.20, passes into a box labelled "
  "ReLU and out to an output circle holding 2.20. Underneath, the whole calculation is written out as "
  "1.0 times 0.5 plus 2.0 times 0.8 plus 0.1 equals 2.20.",
  "0 0 360 200",
  J(line(52, 60, 126, 84, INK, 2),
    line(52, 120, 126, 96, INK, 2),
    t(34, 32, "inputs", 12, MUT, "middle"),
    circ(34, 60, 18, DATA_F, DATA_S, 3),
    t(34, 60, "1.0", 12, INK, "middle", central=True),
    circ(34, 120, 18, DATA_F, DATA_S, 3),
    t(34, 120, "2.0", 12, INK, "middle", central=True),
    t(84, 62, "&#215; 0.5", 12, INK, "middle"),
    t(88, 124, "&#215; 0.8", 12, INK, "middle"),
    t(146, 44, "weighted sum", 12, MUT, "middle"),
    circ(146, 90, 26, PANEL, INK, 3),
    t(146, 90, "sum", 14, INK, "middle", central=True),
    arrow(146, 146, 146, 120, MODEL_S, 2.5),
    t(146, 164, "bias 0.1", 12, INK, "middle"),
    arrow(174, 90, 206, 90, INK, 2.5),
    t(190, 78, "2.20", 12, INK, "middle"),
    t(245, 50, "activation", 12, MUT, "middle"),
    rect(208, 64, 74, 52, 10, MODEL_F, MODEL_S, 3),
    t(245, 90, "ReLU", 14, INK, "middle", central=True),
    arrow(284, 90, 304, 90, OK_S, 2.5),
    t(324, 50, "output", 12, MUT, "middle"),
    circ(324, 90, 20, OK_F, OK_S, 3),
    t(324, 90, "2.20", 12, INK, "middle", central=True),
    t(180, 186, "1.0 &#215; 0.5  +  2.0 &#215; 0.8  +  0.1  =  2.20", 12, MUT, "middle")),
  "The figure's work is the bottom line: the numbers actually being multiplied and added. Without it "
  "this is a flow chart; with it, a reader can check the neuron by hand.")

# ================================================================== layered network
_IN = ((50, 110), (50, 150))
_HID = [(190, y) for y in (70, 100, 130, 160, 190)]
_OUT = (330, 130)
_edges = [line(a[0] + 16, a[1], b[0] - 13, b[1], GRID, 1.5, cap=False)
          for a in _IN for b in _HID]
_edges += [line(h[0] + 13, h[1], _OUT[0] - 18, _OUT[1], GRID, 1.5, cap=False) for h in _HID]

M("motif-network-shapes", "A network with the shapes written between the layers",
  "Two input circles on the left connect to five hidden circles in the middle, which connect to one "
  "output circle on the right. Above the wires, mono labels read W1 2 by 16 and W2 16 by 1. Below each "
  "column, mono labels read 750 by 2, then 750 by 16, then 750 by 1.",
  "0 0 420 270",
  J(t(210, 18, "the batch size 750 never changes; the last number does", 12, MUT, "middle"),
    chip(75, 30, 90, "W1 (2, 16)", MODEL_S, MODEL_F),
    chip(215, 30, 90, "W2 (16, 1)", MODEL_S, MODEL_F),
    _edges,
    [circ(x, y, 16, DATA_F, DATA_S, 3) for x, y in _IN],
    [circ(x, y, 13, MODEL_F, MODEL_S, 3) for x, y in _HID],
    circ(_OUT[0], _OUT[1], 18, OK_F, OK_S, 3),
    t(240, 196, "5 of the 16 drawn", 12, MUT),
    chip(13, 214, 74, "(750, 2)", DATA_S),
    chip(149, 214, 82, "(750, 16)", DATA_S),
    chip(293, 214, 74, "(750, 1)", DATA_S),
    t(50, 258, "2 inputs", 12, MUT, "middle"),
    t(190, 258, "16 hidden units", 12, MUT, "middle"),
    t(330, 258, "1 output", 12, MUT, "middle")),
  "A shape chip under EVERY column, a weight chip over EVERY bundle of wires. If a learner cannot "
  "read the shape off the picture they cannot debug the code. Draw the wires first.")

# ================================================================== forward / backward
_IN2 = ((60, 102), (60, 142))
_HID2 = [(200, y) for y in (72, 106, 140, 174)]
_OUT2 = (340, 122)
_edges2 = [line(a[0] + 16, a[1], b[0] - 12, b[1], GRID, 1.5, cap=False)
           for a in _IN2 for b in _HID2]
_edges2 += [line(h[0] + 12, h[1], _OUT2[0] - 18, _OUT2[1], GRID, 1.5, cap=False) for h in _HID2]

M("motif-forward-backward", "Forward and backward over the same wires",
  "A small network with two inputs, four hidden units and one output. A solid blue arrow runs left to "
  "right above it, labelled forward, numbers flow right, ending at the word output. A dashed pink "
  "arrow runs right to left below it, labelled backward, blame flows left, ending at the word blame.",
  "0 0 420 240",
  J(t(200, 24, "FORWARD &#8212; numbers flow right", 12, DATA_S, "middle"),
    arrow(60, 42, 340, 42, DATA_S, 3),
    t(348, 46, "output", 12, DATA_S),
    _edges2,
    [circ(x, y, 16, DATA_F, DATA_S, 3) for x, y in _IN2],
    [circ(x, y, 12, MODEL_F, MODEL_S, 3) for x, y in _HID2],
    circ(_OUT2[0], _OUT2[1], 18, OK_F, OK_S, 3),
    arrow(340, 196, 60, 196, ACC_S, 3, dash="8 5"),
    t(50, 200, "blame", 12, ACC_S, "end"),
    t(200, 214, "BACKWARD &#8212; blame flows left", 12, ACC_S, "middle"),
    t(200, 230, "the same weights, used twice: forwards, then backwards", 12, MUT, "middle")),
  "Three cues separate the passes, not one: direction of the arrowhead, solid versus dashed, and the "
  "words FORWARD and BACKWARD. Colour is the fourth cue and is never allowed to be the only one.")
