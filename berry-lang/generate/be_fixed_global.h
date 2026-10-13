#include "be_constobj.h"

static be_define_const_map_slots(m_libglobal_map) {
    { be_ckey(undef, -1), be_ckv_func(m_undef) },
    { be_ckey(setmember, 3), be_ckv_func(m_setglobal) },
    { be_ckey(contains, -1), be_ckv_func(m_contains) },
    { be_ckey(member, 4), be_ckv_func(m_findglobal) },
    { be_ckey(_X28_X29, -1), be_ckv_func(m_globals) },
};

static be_define_const_map(
    m_libglobal_map,
    5
);

static be_define_const_module(
    m_libglobal,
    "global"
);

BE_EXPORT_VARIABLE be_define_const_native_module(global);
