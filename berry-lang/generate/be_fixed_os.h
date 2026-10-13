#include "be_constobj.h"

static be_define_const_map_slots(m_libos_map) {
    { be_ckey(listdir, 1), be_ckv_func(m_listdir) },
    { be_ckey(mkdir, -1), be_ckv_func(m_mkdir) },
    { be_ckey(chdir, -1), be_ckv_func(m_chdir) },
    { be_ckey(exit, 2), be_ckv_func(m_exit) },
    { be_ckey(system, -1), be_ckv_func(m_system) },
    { be_ckey(remove, 3), be_ckv_func(m_remove) },
    { be_ckey(path, -1), be_ckv_module(m_libpath) },
    { be_ckey(getcwd, -1), be_ckv_func(m_getcwd) },
};

static be_define_const_map(
    m_libos_map,
    8
);

static be_define_const_module(
    m_libos,
    "os"
);

BE_EXPORT_VARIABLE be_define_const_native_module(os);
