import os.path as osp
from torch_geometric.data import download_url, extract_zip, Dataset, HeteroData
from torch_geometric.transforms import RandomLinkSplit, ToUndirected
import torch_geometric
import pandas as pd 
import torch 

class GenresEncoder:
    def __init__(self, sep='|'):
        self.sep = sep

    def __call__(self, df):
        genres = set(g for col in df.values for g in col.split(self.sep))
        mapping = {genre: i for i, genre in enumerate(genres)}

        x = torch.zeros(len(df), len(mapping))
        for i, col in enumerate(df.values):
            for genre in col.split(self.sep):
                x[i, mapping[genre]] = 1
        return x

class IdentityEncoder:
    def __init__(self, dtype=None):
        self.dtype = dtype

    def __call__(self, df):
        return torch.from_numpy(df.values).view(-1, 1).to(self.dtype)
        
class MovieLensSmall(Dataset):
    def __init__(self, root, transform=None, pre_transform=None, pre_filter=None, filter_threashold=3):
        self.filter_threashold = filter_threashold
        super().__init__(root, transform, pre_transform, pre_filter)
        
    @property
    def raw_file_names(self):
        return ['ml-latest-small/ratings.csv', 'ml-latest-small/movies.csv']

    @property
    def processed_file_names(self):
        return ['data.pt']

    def download(self):
        url = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
        # Download to `self.raw_dir`.
        archive_path = download_url(url, self.raw_dir)
        extract_zip(archive_path, self.raw_dir)
    
    def process(self):
        print(osp.join(self.raw_dir,self.raw_file_names[1]))
        data = HeteroData()
        movie_x, movie_mapping = self.load_node_csv(osp.join(self.raw_dir,self.raw_file_names[1]), "movieId", encoders={"title":GenresEncoder()})
        _, user_mapping = self.load_node_csv(osp.join(self.raw_dir,self.raw_file_names[0]), index_col='userId')
        
        data['user'].num_nodes = len(user_mapping)  # Users do not have any features.
        data['movie'].x = movie_x
        data['movie'].num_nodes = len(movie_mapping)

        edge_index, edge_label = self.load_edge_csv(
            osp.join(self.raw_dir,self.raw_file_names[0]),
            src_index_col='userId',
            src_mapping=user_mapping,
            dst_index_col='movieId',
            dst_mapping=movie_mapping,
            filter_col='rating',
            filter_thr=self.filter_threashold,
            encoders={'rating': IdentityEncoder(dtype=torch.long)},
        )
        data['user', 'rates', 'movie'].edge_index = edge_index
        data['user', 'rates', 'movie'].edge_label = edge_label
        data = ToUndirected()(data)
        del data['movie', 'rev_rates', 'user'].edge_label  # Remove "reverse" label.
        # Save file to disk
        torch.save(data, self.processed_paths[0])
        
    def load_node_csv(self, path, index_col, encoders=None, **kwargs):
        df = pd.read_csv(path, index_col=index_col, **kwargs)
        mapping = {index: i for i, index in enumerate(df.index.unique())}
    
        x = None
        if encoders is not None:
            xs = [encoder(df[col]) for col, encoder in encoders.items()]
            x = torch.cat(xs, dim=-1)
    
        return x, mapping

    def load_edge_csv(self, path, src_index_col, src_mapping, dst_index_col, dst_mapping, filter_col=None, filter_thr=3.0, encoders=None, **kwargs):
        df = pd.read_csv(path, **kwargs)
        # filter out low ratings below the threashold  
        if filter_col is not None: 
            df = df[df[filter_col] >= filter_thr]
        src = [src_mapping[index] for index in df[src_index_col]]
        dst = [dst_mapping[index] for index in df[dst_index_col]]
        edge_index = torch.tensor([src, dst])
    
        edge_attr = None
        if encoders is not None:
            edge_attrs = [encoder(df[col]) for col, encoder in encoders.items()]
            edge_attr = torch.cat(edge_attrs, dim=-1)
    
        return edge_index, edge_attr

    def len(self):
        return len(self.processed_file_names)

    def get(self, idx):
        torch.serialization.add_safe_globals([torch_geometric.data.storage.NodeStorage, HeteroData])
        data = torch.load(osp.join(self.processed_dir, self.processed_file_names[0]), weights_only=False)
        return data