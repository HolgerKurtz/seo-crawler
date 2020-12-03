from tqdm import tqdm

def progress_bar(step, total):
    """takes 2 arguments 'step' to define your step in %
    and "total to define the base like '100' """
    pbar = tqdm(total=total)
    pbar.update(step)
    pbar.close()