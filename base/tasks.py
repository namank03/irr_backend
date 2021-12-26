# Create your tasks here
import json
import time

import numpy_financial as npf
import pandas as pd
from celery import shared_task
from celery_progress.backend import ProgressRecorder


@shared_task(bind=True)
def celery_function(self, data):
    progress_recorder = ProgressRecorder(self)
    df = pd.DataFrame(json.loads(data))
    prn_df = df.filter(like='PRN')
    x3 = df['X3']
    x6 = df['X6']
    x5 = df['X5']
    y1 = x3 * x6
    prn_df = pd.concat([(x3 - y1 + x5) * -1, prn_df], axis=1).convert_dtypes()
    irr_df = pd.concat([df['X1'], prn_df.apply(npf.irr, axis=1) * 100], axis=1).rename(
        columns={0: "IRR"}
    )
    # result = []
    for i in range(len(df)):
        # result.append({"X1": df.iloc[i, 0], "IRR": npf.irr(prn_df.iloc[i, :]) * 100})
        # Simulating the long task behaviour via time.sleep.. If we've a large df we can make the smaller chunks and then we can process that task....
        time.sleep(1)
        progress_recorder.set_progress(i + 1, len(df))

    return json.dumps(irr_df.to_dict('records'))
