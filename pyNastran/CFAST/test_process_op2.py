from IPython.display import display
from pathlib import Path
from pyNastran.op2.op2 import OP2

import pandas as pd

model = OP2(debug=False)

model.read_op2(Path(r'./test_model_cfast.op2'))

# info = model.get_op2_stats()
# print(info)
cfast_forces = model.cfast_force


#for sc in displacements:
#    print(dir(displacements))
#    print(displacements[sc].node_gridtype[:,0])
#    print(displacements[sc].data[0, :, :-3])

df = (pd.concat([(pd.DataFrame(cfast_forces[sc].data[0, :, :], columns=['t1', 't2', 't3', 'r1', 'r2', 'r3'])
                  .assign(Elm = cfast_forces[sc].element[:],
                          SC = sc)
                 )
                for sc in cfast_forces])
      .reset_index(drop=True)
      .reindex(columns=['Elm', 'SC', 't1', 't2', 't3', 'r1', 'r2', 'r3'])
      )
display(df)
