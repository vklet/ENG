import pandas as pd

from pathlib import Path
from pyNastran.op2.op2 import OP2


def get_data(results:dict) -> pd.DataFrame|None:
        return pd.concat((r.data_frame
                          .assign(lc = lc)
                          ) for lc, r in results.items()) if results else None

def main():

        op2_file = Path(r"./bar_grid_point_forces.op2")
        test_model = OP2(debug=False)
        test_model.read_op2(op2_file, build_dataframe=True)
        
        #print(test_model.get_op2_stats())
        #gp_forces = test_model.grid_point_forces[1]

        test_model.print_subcase_key()
        
        gp_forces = get_data(test_model.grid_point_forces)
        displacements = get_data(test_model.displacements)
        bar_stresses = get_data(test_model.cbar_stress)
        #bar_strains = get_data(test_model.cbar_strain)
        beam_stress = get_data(test_model.cbeam_stress)
        #beam_strains= get_data(test_model.cbeam_strain)

        print(displacements)
        print(bar_stresses)
        print(beam_stress)
        print(beam_stress.columns)
        
        test_model.write_f06(op2_file.with_suffix(".f06"))


if __name__ == "__main__":
        main()
