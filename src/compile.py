from kfp.v2 import compiler

from config import COMPILED_PIPELINE_JSON
from pipeline import pipeline

compiler.Compiler().compile(
    pipeline_func=pipeline,
    package_path=f"artifacts/{COMPILED_PIPELINE_JSON}",
)
