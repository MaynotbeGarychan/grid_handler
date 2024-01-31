from src.make_material import make_material_porous_amitex_fftp
from src.make_load import make_load_amitexfftp


coeff_form = [[70.0e+9,0.33,348.0e+6,0.0],
              [0.0,0.0]]
var_form = [[0.0]*13,
            []]

make_material_porous_amitex_fftp("xml_files/material_porous.xml", "/media/chen/ssd/amitex_fftp/libAmitex/src/materiaux/libUmatAmitex.so",
                                 ["elasisoplasvmiso","elasiso"], coeff_form, var_form)

output_ss_list = [1,2,3,4,5,6]
output_Intvar_form = [[13]]
time_discretization_info_form = [["Linear","10","100"]]
output_time_list = [1,2,3,4,5,6,7,8,9]
bc_form = [[0.05,0.0,0.0,0,0,0]]
make_load_amitexfftp("xml_files/load_shearxz.xml", output_ss_list, output_Intvar_form,
                     time_discretization_info_form, output_time_list, bc_form)