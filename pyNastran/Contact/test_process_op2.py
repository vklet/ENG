from IPython.display import display
from pathlib import Path
from pyNastran.op2.op2 import OP2

import pandas as pd

model = OP2(debug=False)

model.read_op2(Path(r'.\contact.op2'))

#info = model.get_op2_stats()
#print(info)
displacements = model.displacements



#for sc in displacements:
#    print(dir(displacements))
#    print(displacements[sc].node_gridtype[:,0])
#    print(displacements[sc].data[0, :, :-3])

df = (pd.concat([(pd.DataFrame(displacements[sc].data[0, :, :-3], columns=['t1', 't2', 't3'])
                  .assign(Node = displacements[sc].node_gridtype[:, 0],
                          SC = sc)
                 )
                for sc in displacements])
      .reindex(columns=['Node', 'SC', 't1', 't2', 't3'])
      )
display(df)
#print(model.table_names)
