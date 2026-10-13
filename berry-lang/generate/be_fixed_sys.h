#include "be_constobj.h"

static be_define_const_map_slots(m_libsys_map) {
    { be_ckey(path, -1), be_ckv_func(m_path) },
};

static be_define_const_map(
    m_libsys_map,
    1
);

static be_define_const_module(
    m_libsys,
    "sys"
);

BE_EXPORT_VARIABLE be_define_const_native_module(sys);
