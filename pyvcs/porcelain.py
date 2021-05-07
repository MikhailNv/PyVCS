import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths)

def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    commit_sha = commit_tree(gitdir, write_tree(gitdir, read_index(gitdir)), message, author = author)
    if is_detached(gitdir):
        ref = gitdir / "HEAD"
    else:
        ref = pathlib.Path(get_ref(gitdir))
    with pathlib.Path(gitdir, ref).open("w") as f:
        f.write(commit_sha)
        f.close()
    return commit_sha


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    ref = get_ref(gitdir)
    if os.path.isfile(gitdir/ref):
        with pathlib.Path(gitdir/ref).open("r") as f:
            ref = f.read()
            f.close()
    fmt, content = read_object(ref, gitdir)
    content = content.decode()
    #print(content)
    objects = find_tree_files(content[5:45], gitdir)
    dirs = gitdir.absolute().parent
    for obj in objects:
        os.remove(dirs / obj[0])
        next_path = pathlib.Path(obj[0]).parent 
        while len(next_path.parents) > 0:
            os.rmdir(next_path)
            next_path = pathlib.Path(next_path).parent
    with pathlib.Path(gitdir / "HEAD").open("w") as f:
        f.write(obj_name)
        f.close()    
    fmt, new_content = read_object(obj_name, gitdir)
    new_content = new_content.decode()
    objects = find_tree_files(new_content[5:45], gitdir)
    for i in objects:
        z = len(pathlib.Path(obj[0]).parents)
        par_path = dirs
        for par in range(z - 2, -1, -1):
            par_path /= pathlib.Path(i[0]).parents[par]
            if not os.path.isdir(par_path):
                os.mkdir(par_path)
        #print(i[0], ' ', i[1])
        fmt, obj_content = read_object(i[1], gitdir)
        if fmt == "blob":
            pathlib.Path(dirs / i[0]).touch()
            with pathlib.Path(dirs / i[0]).open("w") as f:
                f.write(obj_content.decode())
                f.close()
        else:
            os.mkdir(dirs / i[0])