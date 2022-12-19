import dataclasses

from api.features.filepaths.domain.values import RecordingMeta

@dataclasses.dataclass
class Recording:
    meta: RecordingMeta
    tmp_blob_path: str
    retries: int

