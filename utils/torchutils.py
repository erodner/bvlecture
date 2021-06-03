import torch
import shutil

try:
    import torchviz
    if shutil.which("dot") is None:
        torchviz_disabled = True
    else:
        torchviz_disabled = False
    
except:
    torchviz_disabled = True


def make_dot(target_variable, other_variables={}, **kwargs):
    if torchviz_disabled:
        print ("You need to install the module torchviz (by pip) & graphviz for visualization")
        return ""
    else:
        if not "params" in kwargs:
            all_local_tensors = { f: v for f, v in other_variables.items() \
                                 if isinstance(v, torch.Tensor) and not f.startswith("_") }
            
            return torchviz.make_dot(target_variable, params=all_local_tensors, **kwargs)
        else:
            return torchviz.make_dot(target_variable, **kwargs)