"""Runnable usage examples for the verification harness.

Each module under ``examples/`` is executable with either:

    python examples/run_verification.py
    python -m examples.run_verification

Modules here must not perform any pipeline work at import time.
All work lives in ``main()`` and is guarded by ``if __name__ == '__main__'``.
"""
