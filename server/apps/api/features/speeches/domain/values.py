import dataclasses

from ...filepaths import RecordingMeta

@dataclasses.dataclass
class Recording:
    meta: RecordingMeta
    tmp_blob_path: str
    retries: int

