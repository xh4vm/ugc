import os

from pandas import read_csv


class DatasetLoader:
    file_name = ''
    column_types: dict = {}
    error = None

    def __init__(
            self,
            batch_size: int,
            dataset_folder: str,
            dataset_file_ext: str,
            dataset_data_deliver: str,
            dataset_data_skip_row: int,
    ):
        self.batch_size = batch_size
        self.dataset_folder = dataset_folder
        self.dataset_file_ext = dataset_file_ext
        self.dataset_data_deliver = dataset_data_deliver
        self.dataset_data_skip_row = dataset_data_skip_row

    def load_batch(self):
        for batch in read_csv(
                self.file_name,
                engine='python',
                sep=self.dataset_data_deliver,
                header=None,
                skiprows=self.dataset_data_skip_row,
                chunksize=self.batch_size,
                dtype=self.column_types,
        ):
            yield [tuple(value) for value in batch.values.tolist()]

    def load_one_file(self, file_name: str, types: dict):
        path_file = os.sep.join([self.dataset_folder, '{0}.{1}'.format(file_name, self.dataset_file_ext)])
        if not os.path.exists(path_file):
            self.error = 'The file {0} does not exist.'.format(path_file)
            return False
        self.file_name = path_file
        self.column_types = types
        return True
