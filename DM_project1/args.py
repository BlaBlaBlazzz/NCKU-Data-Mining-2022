import argparse

def parse_args():
    p = argparse.ArgumentParser()

    def a(*args, **kwargs):
        p.add_argument(*args, **kwargs)

    def k(*args, **kwargs):
        p.add_argument(*args, **kwargs)

    a('--min_sup', type=float, default=0.1, help='Minimum support')
    a('--min_conf', type=float, default=0.1, help='Minimum confidence')
    a('--dataset', type=str, default='2022-DM-release-testdata-2.txt', help='Dataset to use, please include the extension')

    k('--min_sup_k', type=float, default=0.5, help='Minimum support')
    k('--min_conf_k', type=float, default=0.8, help='Minimum confidence')
    k('--dataset_k', type=str, default='kaggle-Bollywood Movies Dataset.csv', help='Dataset to use, please include the extension')

    #2022-DM-release-testdata-2
    return p.parse_args()