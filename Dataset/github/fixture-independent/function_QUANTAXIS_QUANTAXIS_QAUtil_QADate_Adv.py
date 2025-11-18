from datetime import datetime, timezone, timedelta
import numpy as np

def QA_util_timestamp_to_str(ts_epoch=None, local_tz=timezone(timedelta(hours=8))):
    if ts_epoch is None:
        ts_epoch = datetime.now(timezone(timedelta(hours=8)))
    if isinstance(ts_epoch, datetime):
        try:
            return ts_epoch.astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return ts_epoch.tz_localize(local_tz).strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(ts_epoch, int) or isinstance(ts_epoch, np.int32) or isinstance(ts_epoch, np.int64) or isinstance(ts_epoch, float):
        return (datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=int(ts_epoch))).astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')
    else:
        raise Exception('No support type %s.' % type(ts_epoch))