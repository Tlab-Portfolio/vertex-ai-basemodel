from datetime import datetime

import google.cloud.aiplatform as aip

from config import BUCKET_URI, COMPILED_PIPELINE_JSON, PIPELINE_ROOT, PROJECT_ID, REGION

JOB_DISPLAY_NAME = "cal_housing_" + datetime.now().strftime("%Y%m%d_%H%M%S")


aip.init(project=PROJECT_ID, location=REGION, staging_bucket=BUCKET_URI)


job = aip.PipelineJob(
    display_name=JOB_DISPLAY_NAME,
    template_path=f"artifacts/{COMPILED_PIPELINE_JSON}",
    pipeline_root=PIPELINE_ROOT,
    enable_caching=False,
    # parameter_values={"param_name": value}, # Use this argment if pipline() takes argments.
)

job.run()
