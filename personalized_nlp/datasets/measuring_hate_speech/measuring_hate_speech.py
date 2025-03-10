import os

from pathlib import Path
from typing import List

import pandas as pd

from settings import DATA_DIR
from personalized_nlp.utils.data_splitting import split_texts
from personalized_nlp.datasets.datamodule_base import BaseDataModule


class MeasuringHateSpeechDataModule(BaseDataModule):

    @property
    def annotations_file(self) -> str:
        return f'annotations.tsv'

    @property
    def data_file(self) -> str:
        return f'data.tsv'

    @property
    def data_dir(self) -> Path:
        return DATA_DIR / "measuring_hate_speech"

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

        os.makedirs(self.data_dir / "embeddings", exist_ok=True)

    def prepare_data(self) -> None:
        self.data = pd.read_csv(self.data_dir / self.data_file)

        self.annotators = pd.read_csv(
            self.data_dir / "worker_demographics.tsv",
            sep="\t",
        )

        self.annotations = pd.read_csv(self.data_dir / self.annotations_file)

    @property
    def class_dims(self) -> List[int]:
        return [5, 5, 5, 5, 5, 5, 5, 5, 5, 3]

    @property
    def annotation_columns(self) -> List[str]:
        return [
            "sentiment", "respect", "insult", "humiliate", "status",
            "dehumanize", "violence", "genocide", "attack_defend", "hatespeech"
        ]

    @property
    def embeddings_path(self) -> Path:
        return (self.data_dir /
                f"embeddings/rev_id_to_emb_{self.embeddings_type}.p")
