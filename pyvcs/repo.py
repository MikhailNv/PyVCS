import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    try:
        env = os.environ['GIT_DIR']
        path = pathlib.Path(workdir).absolute() 
        if workdir == env:
            return pathlib.Path(workdir).absolute() 
        t = 0
        for dirpath, dirnames, filenames in os.walk(workdir):
            for name in dirnames:
                a = os.path.join(dirpath, name)
                if name == env:
                    global z
                    t = 1
                    z = pathlib.Path(os.path.join(dirpath, name)).absolute()
                    break
            if t == 1:
                break
        if t == 0:
            parent = os.path.dirname(workdir)
            repo_find(parent)
        return z
    except Exception:
        raise AssertionError("Not a git repository")
                    #print(pathlib.Path(os.path.join(dirpath, a2)).absolute())
                    #return (pathlib.Path(os.path.join(dirpath, a2)).absolute())             
                
                
    #    parent = os.path.dirname(workdir)
    #    repo_find(parent)
    #repo_find(parent)
    #print(parent)
    #return (pathlib.Path(parent).absolute())
        
    #return pathlib.Path().absolute()
    
    #a=[str(x) for x in p.iterdir() if x.is_dir()]
    #print(a)
    #for i in a:
    #    if ".git" in i:
    #        return pathlib.Path(i).absolute()
    #expected_gitdir = p / ".git"
    #if pathlib.Path(expected_gitdir).exists():
    #if pathlib.Path(pa).exists():
    
    #x = x.absolute()
    #print(x)
    
    #print(expected_gitdir)
    """
    p = pathlib.Path('.')
    a=[str(x) for x in p.iterdir() if x.is_dir()]
    for i in range(len(a)):
        if workdir == str(a[i]):
            return True
        else:
            return False
    """
def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    if "GIT_DIR" not in os.environ:
        os.environ["GIT_DIR"] = ".git"
    env = os.environ["GIT_DIR"]
    if pathlib.Path(workdir).is_dir():
        p = pathlib.Path(workdir)
        if not os.path.exists(p / env):
            os.mkdir(p/env)
        elif not os.path.exists(pathlib.Path(p/env/"refs")):
            os.makedirs(p/env/"refs")
        elif not os.path.exists(pathlib.Path(p/env/"refs/tags")):
            os.mkdir(p/env/"refs"/"tags")
        elif not os.path.exists(pathlib.Path(p/env/"refs/heads")):
            os.makedirs(p/env/"refs"/"heads")
        elif not os.path.exists(pathlib.Path(p/env/"objects")):
            os.mkdir(p/env/"objects")         
        elif not os.path.exists(pathlib.Path(p/env/"HEAD")):
            pathlib.Path(p/env/"HEAD").touch()
            file = open(pathlib.Path(p/env/"HEAD"), "w")
            file.write("ref: refs/heads/master\n")
            file.close()
        elif not os.path.exists(pathlib.Path(p/env/"config")):
            pathlib.Path(p/env/"config").touch()
            file = open(pathlib.Path(p/env/"config"), "w")
            file.write("[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n")
            file.close()
        elif not os.path.exists(pathlib.Path(p/env/"description")):
            pathlib.Path(p/env/"description").touch()
            file = open(pathlib.Path(p/env/"description"), "w")
            file.write("Unnamed pyvcs repository.\n")
            file.close()         
        #print(pathlib.Path(env).absolute())
        return pathlib.Path(env)
    else:
        raise AssertionError(f"{workdir} is not a directory") 


#print(repo_create("."))
