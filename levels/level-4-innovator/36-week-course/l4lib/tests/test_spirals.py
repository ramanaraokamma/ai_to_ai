"""Plain-assert tests for l4lib/spirals.py.  Run: python3 tests/test_spirals.py"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import spirals


def test_shapes_and_dtypes():
    X, y = spirals.make_spirals()
    assert X.shape == (1200, 2) and y.shape == (1200,)
    assert X.dtype == np.float32 and y.dtype == np.int64
    assert set(y.tolist()) == {0, 1} and int(y.sum()) == 600


def test_seeded_and_different_across_seeds():
    a, ay = spirals.make_spirals(100, 0.2, seed=3)
    b, by = spirals.make_spirals(100, 0.2, seed=3)
    c, _ = spirals.make_spirals(100, 0.2, seed=4)
    assert np.array_equal(a, b) and np.array_equal(ay, by)
    assert not np.array_equal(a, c)


def test_noise_zero_is_on_the_curve():
    X, y = spirals.make_spirals(50, 0.0, seed=0)
    r = np.hypot(X[:, 0], X[:, 1])
    assert r.min() >= 0.35 - 1e-5 and r.max() <= 3.4 + 1e-5


def test_data_split_840_360_standardized_on_train():
    Xtr, ytr, Xva, yva = spirals.get_data()
    assert tuple(Xtr.shape) == (840, 2) and tuple(Xva.shape) == (360, 2)
    assert abs(float(Xtr.mean())) < 1e-5
    assert abs(float(Xtr.std(0)[0]) - 1.0) < 1e-4
    assert float(Xva.mean()) != 0.0          # val uses TRAIN stats, so not exactly 0


def test_run_is_deterministic_and_learns():
    h1 = spirals.run("t", epochs=3, verbose=False)
    h2 = spirals.run("t", epochs=3, verbose=False)
    assert h1["train"] == h2["train"] and h1["val"] == h2["val"]
    assert len(h1["train"]) == 3 and set(h1) == {"train", "val", "acc", "lr", "gnorm"}
    assert h1["train"][-1] < h1["train"][0]


def test_depth_argument_changes_model():
    n4 = sum(p.numel() for p in spirals.make_model(depth=4).parameters())
    n8 = sum(p.numel() for p in spirals.make_model(depth=8).parameters())
    assert n8 - n4 == 4 * (64 * 64 + 64)


def test_schedule_and_residual_options_run():
    h = spirals.run("t", epochs=2, schedule="cosine", warmup_frac=0.1, norm="layer",
                    residual=True, clip=1.0, verbose=False)
    assert h["lr"][0] > h["lr"][-1] >= 0


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for f in tests:
        f()
    print(f"spirals: all {len(tests)} tests passed")
