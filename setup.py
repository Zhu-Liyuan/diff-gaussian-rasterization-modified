# setup.py - minimal, H200 (compute 10.0 / sm_100) specific
from setuptools import setup
from torch.utils.cpp_extension import CUDAExtension, BuildExtension
import os

here = os.path.dirname(os.path.abspath(__file__))
glm_include = "-I" + os.path.join(here, "third_party", "glm")

# NVCC gencode flags for H200 (compute 10.0 -> 100)
nvcc_gencode_flags = [
    "-gencode=arch=compute_100,code=sm_100",
    "-gencode=arch=compute_100,code=compute_100",  # PTX fallback
]

extra_nvcc_args = ["--extended-lambda"] + nvcc_gencode_flags + [glm_include]

setup(
    name="diff_gaussian_rasterization",
    packages=['diff_gaussian_rasterization'],
    ext_modules=[
        CUDAExtension(
            name="diff_gaussian_rasterization._C",
            sources=[
                "cuda_rasterizer/rasterizer_impl.cu",
                "cuda_rasterizer/forward.cu",
                "cuda_rasterizer/backward.cu",
                "rasterize_points.cu",
                "ext.cpp"
            ],
            extra_compile_args={"nvcc": extra_nvcc_args}
        )
    ],
    cmdclass={'build_ext': BuildExtension}
)
