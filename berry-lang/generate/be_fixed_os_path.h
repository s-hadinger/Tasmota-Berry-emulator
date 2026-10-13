#include "be_constobj.h"

static be_define_const_map_slots(m_libpath_map) {
    { be_ckey(isdir, -1), be_ckv_func(m_path_isdir) },
    { be_ckey(join, 2), be_ckv_func(m_path_join) },
    { be_ckey(exists, -1), be_ckv_func(m_path_exists) },
    { be_ckey(split, -1), be_ckv_func(m_path_split) },
    { be_ckey(splitext, -1), be_ckv_func(m_path_splitext) },
    { be_ckey(isfile, -1), be_ckv_func(m_path_isfile) },
};

static be_define_const_map(
    m_libpath_map,
    6
);

static be_define_const_module(
    m_libpath,
    "path"
);

BE_EXPORT_VARIABLE be_define_const_native_module(path);
