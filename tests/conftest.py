# pytest configuration for SignBridge tests
# On Windows, pre-importing torch at pytest session startup ensures PyTorch's
# c10.dll / OpenMP runtimes are cleanly loaded before threadpool/scikit-learn routines.
try:
    import torch  # noqa: F401
except Exception:
    pass

